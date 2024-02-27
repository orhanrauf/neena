import openai
import instructor

from typing import Any
from fastapi import Depends
from sqlalchemy.orm import Session
from openai.types.chat.chat_completion import ChatCompletion

from app.core.config import settings
from app.schemas.flow import FlowBase
from app.schemas.task_definition import TaskDefinition
from app.schemas.task_operation import TaskOperationBase
from app.schemas.dependency import DependencyBase, DependencyList
from app.schemas.flow import FlowBase
from app.crud.crud_task_definition import task_definition
from app.core.logging import logger
from app.db.session import SessionLocal
from app.api import deps


class FlowGenerator:
    """
    Class that handles user request, and generates and returns
    formatted flow for execution layer.
    """

    def __init__(
        self,
        openai_api_key: str = settings.OPENAI_API_KEY,
        model: str = "gpt-4",
    ) -> None:
        # TODO: consolidate OpenAI config, prompt handling into separate classes
        self.model = model
        self.client = instructor.patch(openai.OpenAI(api_key=openai_api_key))
        self.database = SessionLocal()

    def generate_flow_from_request(self, request: str) -> Any:
        """
        Main entry point of class.
        Accepts: request (str).
        Returns: flow (FlowBase)
        """
        # [DUMMY STEP] collection of TaskDefinition's = self.from_request_determine_task_definitions_using_rag(request) / Communicates with database / TaskDefinitionGetter (API Call 1)
        task_definitions = self.get_requested_task_definitions_from_database(request)
        task_operations = self.convert_task_definitions_to_task_operations(task_definitions)
        # flow = self.generate_flow_from_requested_task_definitions(request, task_definitions)
        # flow = self.generate_flow_from_request_given_task_definitions(request, list[TaskDefinition]) (API Call 2)
        # return flow
        dependencies = self.generate_flow_from_requested_task_operations(
            request=request, requested_task_operations=task_operations
        )
        return self._construct_flow_from_task_operations_and_dependencies(task_operations, dependencies)

    def get_requested_task_definitions_from_database(self, request: str) -> list[TaskDefinition]:
        # Consider moving this to its own class;
        # e.g., TaskDefinitionRetriever, TaskDefinitionGetter
        # TODO: This is where eventually the RAG happens:
        # #### This method (later will become a class) interprets the request using RAG (i.e., 1 API call)
        # #### so it knows which TaskDefinitions it can and should get from the database
        # requested_task_definitions = ["Get Boards", "Get List", "Get Card", "Update Card"]
        requested_task_definitions = ["Get Boards", "Get List", "Get Card", "Delete Card"]
        return task_definition.get_by_names(db=self.database, task_definition_names=requested_task_definitions)

    def convert_task_definitions_to_task_operations(
        self, requested_task_definitions: list[TaskOperationBase]
    ) -> list[TaskOperationBase]:
        task_operations = [
            TaskOperationBase(
                name=requested_task_definiton.task_name,
                task_definition=requested_task_definiton.id,
                instruction=f"Instruction {task_operation_index}",
                index=task_operation_index,
            )
            for task_operation_index, requested_task_definiton in enumerate(requested_task_definitions)
        ]
        return task_operations

    def generate_flow_from_requested_task_operations(
        self, request: str, requested_task_operations: list[TaskOperationBase]
    ) -> Any:

        example_dependencylist_obj = DependencyList(
            dependencies=[
                DependencyBase(instruciton="instruction string body", source_task_operation=1, target_task_operation=4)
            ]
        )

        dumped_obj = example_dependencylist_obj.model_dump()

        dumped_obj_str = str(dumped_obj)

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
        # You must return and instance of class DepencencyList, which is a list of dependencies in the following form:
        #             dependencies = [
        #                 DependencyBase(instruction="[INSTRUCTION ABOUT DEPENDENCY 0 (must be str)]", source_task_operation=[SOURCE TASK OPERATION INDEX (must be int)], target_task_operation=[SOURCE TASK OPERATION INDEX (must be int)]),
        #                 ...,
        #                 DependencyBase(instruction="[INSTRUCTION ABOUT DEPENDENCY N (must be str)]", source_task_operation=[SOURCE TASK OPERATION INDEX (must be int)], target_task_operation=[SOURCE TASK OPERATION INDEX (must be int)]),
        #             ]
        print(f"REQUEST: {request}")
        print(f"LIST OF TASK OPERATIONS: {requested_task_operations}")
        # print(f"TASK OPERATIONS: {requested_task_operations}")
        # chat_completion = self._create_chat_completion_for_messages(messages)
        # return self._extract_last_message_from_chat_completion(chat_completion)
        return self._create_chat_completion_for_messages(messages)

    def _create_chat_completion_for_messages(self, messages: list) -> Any:
        try:
            # chat_completion = self.client.chat.completions.create(
            #     model=self.model, response_model=list[DependencyBase], messages=messages
            # )
            # return chat_completion
            dependencies = self.client.chat.completions.create(
                model=self.model,
                response_model=DependencyList,
                messages=messages,
                # response_format={"type": "json_object"},
            )
            print(f"DEPENDENCIES: {dependencies}")
            dumped_dependendies = dependencies.model_dump()
            print(f"DUMPED DEPENDENCIES: {str(dumped_dependendies)}")
            assert isinstance(dependencies, DependencyList)
            # assert isinstance(dependencies.dependencies, list[DependencyBase])
            return dependencies
        except openai.APIConnectionError as e:
            logger.error("The server could not be reached")
            logger.error(e.__cause__)
        except openai.RateLimitError as e:
            logger.error("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            logger.error("Another non-200-range status code was received")
            logger.error(e.status_code)
            logger.error(e.response)

    def _extract_last_message_from_chat_completion(self, chat_completion) -> str:
        return chat_completion.choices[0].message.content

    def _construct_flow_from_task_operations_and_dependencies(
        self, task_operations: list[TaskOperationBase], dependencies: DependencyList
    ) -> FlowBase:
        flow = FlowBase(name="Hello, world", task_operations=task_operations, dependencies=dependencies.dependencies)
        print(f"FLOW: {flow}")
        assert isinstance(flow, FlowBase)
        return flow


flow_generator = FlowGenerator()

# find update the project planning card by adding the following item: "migrate database"
# find and delete the project planning card about migrating the sql database
# Get Board, Get List, Update Card
