import openai
import instructor

from sqlalchemy.orm import Session

from app.core.logging import LoggerConfigurator
from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.crud_task_definition import task_definition
from app.schemas import (
    FlowBase,
    TaskDefinition,
    TaskDefinitionNamesList,
    TaskOperationBase,
    DependencyBase,
    DependencyList,
)

logger = LoggerConfigurator.configure_logger(__name__)


class PatchedOpenAIClient:
    """
    A client for interfacing with OpenAI's API using a patched version of the OpenAI client.

    This class wraps the OpenAI client provided by the `openai` library, applying a custom patch
    via the `instructor` module. It is designed to facilitate making chat completion requests to
    the OpenAI API, handling any errors that may arise during the request process.

    Attributes:
        client (openai.OpenAI): The patched OpenAI client instance configured with the provided API key.

    Args:
        api_key (str): The API key for authenticating requests to OpenAI's API.
    """

    def __init__(self, api_key: str) -> None:
        self.client = instructor.patch(openai.OpenAI(api_key=api_key))

    def create_chat_completion(self, model: str, messages: list[dict]) -> DependencyList:
        """
        Creates a chat completion request to the OpenAI API using the specified model and message sequence.

        This method sends a request to the OpenAI API to generate chat completions based on a sequence
        of messages. It is designed to handle and log any errors encountered during the request process,
        raising exceptions for any unhandled errors to be addressed by the calling context.

        Args:
            model (str): The model to be used for generating chat completions (e.g., "gpt-4" or "gpt-3.5-turbo").
            messages (list[dict]): A list of message dictionaries representing the conversation history,
                                   where each message is a dict with keys "role" (str) and "content" (str).

        Returns:
            DependencyList: An instance of DependencyList containing the generated chat completions.

        Raises:
            openai.Error: If an error occurs during the request to the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=model, messages=messages, response_model=DependencyList
            )
            return response
        except openai.Error as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class TaskGetterPatchedOpenAIClient:
    """
    A client for interfacing with OpenAI's API using a patched version of the OpenAI client.

    This class wraps the OpenAI client provided by the `openai` library, applying a custom patch
    via the `instructor` module. It is designed to facilitate making chat completion requests to
    the OpenAI API, handling any errors that may arise during the request process.

    Attributes:
        client (openai.OpenAI): The patched OpenAI client instance configured with the provided API key.

    Args:
        api_key (str): The API key for authenticating requests to OpenAI's API.
    """

    def __init__(self, api_key: str) -> None:
        self.client = instructor.patch(openai.OpenAI(api_key=api_key))

    def create_chat_completion(self, model: str, messages: list[dict]) -> TaskDefinitionNamesList:
        """
        Creates a chat completion request to the OpenAI API using the specified model and message sequence.

        This method sends a request to the OpenAI API to generate chat completions based on a sequence
        of messages. It is designed to handle and log any errors encountered during the request process,
        raising exceptions for any unhandled errors to be addressed by the calling context.

        Args:
            model (str): The model to be used for generating chat completions (e.g., "gpt-4" or "gpt-3.5-turbo").
            messages (list[dict]): A list of message dictionaries representing the conversation history,
                                   where each message is a dict with keys "role" (str) and "content" (str).

        Returns:
            TaskDefinitionNamesList: An instance of TaskDefinitionNamesList...

        Raises:
            openai.Error: If an error occurs during the request to the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=model, messages=messages, response_model=TaskDefinitionNamesList
            )
            return response
        except openai.Error as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class FlowGenerator:
    """
    Worker class containing logic for Flow generation for natural language requests.
    """

    def __init__(
        self,
        task_getter_client: TaskGetterPatchedOpenAIClient,
        patched_openai_client: PatchedOpenAIClient,
        database_session: Session,
        model: str = "gpt-4",
    ) -> None:
        self.model = model
        self.task_getter_client = task_getter_client
        self.patched_openai_client = patched_openai_client
        self.database_session = database_session

    def generate_flow_from_request(self, request: str) -> FlowBase:
        """
        Main entry point of class.
        Generates and returns formatted flow for execution layer based on user requests.

        Args:
            request (str): Natural language request from user describing flow to be generatored.

        Returns:
            flow (FlowBase): Flow DAG-form with task operations (nodes) and dependencies (edges, vertices).
        """
        task_definitions = self._get_task_definitions_from_database(request)
        requested_task_operations = self._convert_task_definitions_to_task_operations(task_definitions)
        dependencies = self._generate_dependencies(request, requested_task_operations)
        return self._construct_flow(requested_task_operations, dependencies)

    def _get_task_definitions_from_database(self, request: str) -> list[TaskDefinition]:
        # TODO: Placeholder for actual task definition retrieval logic
        all_task_definiton_names = [
            "Create Board",
            "Create Card",
            "Create List",
            "Delete Board",
            "Delete Card",
            "Get Board",
            "Get Boards",
            "Get Card",
            "Get Cards in List",
            "Get List",
            "Get Lists in Board",
            "Update Board",
            "Update Card",
            "Update List",
        ]
        messages = [
            {
                "role": "system",
                "content": """
                    You are part of an application that enables its users to construct and automate complex flows in Trello. 
                    The user will give you a natural language request describing the desired overarching flow to be constructed.
                    
                    You must select the necessary tasks to construct the flow requested by the user.
                    You can only select tasks from the given exhaustive list of permissible task names.
                    Your response is considered incorrect if it contains a task name that is not in the list of permissible names.
                    Incorrect responses result in the application breaking.
                    
                    List of permissible task names:
                        Create Board
                        Create Card
                        Create List
                        Delete Board
                        Delete Card
                        Get Board
                        Get Boards
                        Get Card
                        Get Cards in List
                        Get List
                        Get Lists in Board
                        Update Board
                        Update Card
                        Update List
                    
                    You must only return a list containing the task names, perserving the capitalization as shown in the list.
                    The list cannot contain any duplicate elements.
                    Your response must solely consist of the desired list. 
                    Do not add anything else to your response, because it will impede the extraction process of subsequent modules. 
                    Your output must adhere to the following format:
                    
                    ["Task Name 1", "Task Name 2", ..., "Task Name 3"]
                    
                """,
            },
            {"role": "user", "content": "Find and delete the project planning card about migrating the sql database."},
            {"role": "assistant", "content": '["Get Boards", "Get List", "Get Card", "Delete Card"]'},
            {"role": "user", "content": f"{request}"},
        ]
        requested_task_definitions_names = self.task_getter_client.create_chat_completion(self.model, messages)
        return task_definition.get_by_names(self.database_session, requested_task_definitions_names.task_definitions)

    def _convert_task_definitions_to_task_operations(
        self, task_definitions: list[TaskOperationBase]
    ) -> list[TaskOperationBase]:
        return [
            TaskOperationBase(
                name=task_definiton.task_name,
                task_definition=task_definiton.id,
                instruction=f"Instruction {index}",
                index=index,
            )
            for index, task_definiton in enumerate(task_definitions)
        ]

    def _generate_dependencies(
        self, request: str, requested_task_operations: list[TaskOperationBase]
    ) -> DependencyList:
        messages = [
            {
                "role": "system",
                "content": """
                    You are part of an application that enables its users to automate complex tasks in Trello. 
                    The user will give you a natural language request describing the desired overarching task to be completed. 
                    The user will also give you a list of instances of a class called TaskOperationBase.
                    TaskOperationBase is defined as follows:
                    TaskOperationBase(
                        name="[TASK OPERATION NAME]",
                        task_definition="[TASK ID]",
                        instruction="[OPTIONAL USER PROVIDED ADDITIONAL INSTRUCTIONS]",
                        index=[UNIQUE INTEGER IDENTIFIER OF TASK OPERATION],
                    )
                    
                    Based on the user-provided request and list of task operations, you must form a valid Directed Acyclic Graph (DAG) by connecting the given task operations by edges referred to as dependencies.
                    You must return the list of dependencies between task operations in valid JSON format as demonstrated below:
                    {
                    "dependencies":[
                        {
                            "instruction": <string instruction body that explains dependency between source and target task operation>,
                            "source_task_operation": <int source task operation index>,
                            "target_task_operation":<int target task operation index>
                        },
                        ...
                        {
                            "instruction": <string instruction body that explains dependency between source and target task operation>,
                            "source_task_operation": <int source task operation index>,
                            "target_task_operation":<int target task operation index>
                        }
                    ]
                    }
                """,
            },
            {
                "role": "user",
                "content": """
                Request: find and update the project planning card by adding the following item: "migrate database"
                
                List of task operations: [TaskOperationBase(name='Get Card', task_definition=UUID('9e7eaf56-3854-4798-8df4-f62bb4250dd9'), instruction='Instruction 0', x=None, y=None, index=0), TaskOperationBase(name='Get List', task_definition=UUID('24fe857e-82b1-4588-9fa9-b9cd19a7fbd1'), instruction='Instruction 1', x=None, y=None, index=1), TaskOperationBase(name='Get Boards', task_definition=UUID('026dce4d-33ad-4bcb-99a7-eaf69cb9c01a'), instruction='Instruction 2', x=None, y=None, index=2), TaskOperationBase(name='Update Card', task_definition=UUID('a9df78a5-9c28-4c9c-981a-280eef2e5626'), instruction='Instruction 3', x=None, y=None, index=3)]
                """,
            },
            {
                "role": "assistant",
                "content": """
                {
                    "dependencies":[
                        {
                            "instruction":"Get Boards before anything else",
                            "source_task_operation":3,
                            "target_task_operation":1
                        },
                        {
                            "instruction":"Get List after Get Boards",
                            "source_task_operation":1,
                            "target_task_operation":0
                        },
                        {
                            "instruction":"Get Card after Get List",
                            "source_task_operation":0,
                            "target_task_operation":2
                        }
                    ]
                    }
                """,
            },
            {
                "role": "user",
                "content": f"""
                    Request: {request}
                    
                    List of task operations: {requested_task_operations}
                 """,
            },
        ]
        dependencies = self.patched_openai_client.create_chat_completion(self.model, messages)
        return dependencies

    def _construct_flow(self, task_operations: list[TaskOperationBase], dependencies: DependencyList) -> FlowBase:
        flow = FlowBase(name="Hello, world", task_operations=task_operations, dependencies=dependencies.dependencies)
        return flow


database_session = SessionLocal()
patched_openai_client = PatchedOpenAIClient(settings.OPENAI_API_KEY)
task_getter_client = TaskGetterPatchedOpenAIClient(settings.OPENAI_API_KEY)
flow_generator = FlowGenerator(
    task_getter_client=task_getter_client,
    patched_openai_client=patched_openai_client,
    database_session=database_session,
)

# Example requests to test with:
# find update the project planning card by adding the following item: "migrate database"
# find and delete the project planning card about migrating the sql database
