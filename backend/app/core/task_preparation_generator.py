from typing import Any, List
import instructor
import openai

from app.core.config import settings
from app.core.logging import logger
from app.db.session import SessionLocal
from app.schemas.task_prep_prompt import TaskPrepPromptBase
from app.schemas.flow import Flow
from app.schemas.flow_run import FlowRun
from app.schemas.task_definition import TaskDefinition
from app.schemas.task_operation import TaskOperationBase
from app.schemas.task_prep_answer import TaskPrepAnswerBase


class TaskPreparationGenerator:
    """
    This class is responsible for preparing the parameters for a TaskOperation
    given the state of a Flow execution, Flow graph and previous TaskOperation outputs.
    """

    def __init__(
        self,
        openai_api_key: str = settings.OPENAI_API_KEY,
        model: str = "gpt-4-0125-preview",
    ) -> None:
        self.model = model
        self.client = instructor.patch(openai.OpenAI(api_key=openai_api_key))
        self.database = SessionLocal()

    def generate(
        self, flow: Flow, flow_run: FlowRun, task_operation_index: int, task_definition: TaskDefinition
    ) -> tuple[TaskPrepPromptBase, TaskPrepAnswerBase]:
        """
        Generates a prompt for the task preparation and sends it to the OpenAI API to generate an answer.
        """
        task_prep_prompt = self._create_task_prep_prompt(flow, flow_run, task_operation_index, task_definition)
        task_prep_answer = self._create_task_prep_answer(task_prep_prompt)

        return task_prep_prompt, task_prep_answer

    def _create_task_prep_answer(self, task_prep_prompt: TaskPrepPromptBase) -> TaskPrepAnswerBase:
        """
        Creates a task preparation answer based on the given task preparation prompt.

        Args:
            task_prep_prompt (TaskPrepPromptBase): The task preparation prompt.

        Returns:
            TaskPrepAnswerBase: The generated task preparation answer.
        """
        try:
            task_prep_answer = self.client.chat.completions.create(
                model=self.model, response_model=TaskPrepAnswerBase, messages=task_prep_prompt.messages
            )
            assert isinstance(task_prep_answer, TaskPrepAnswerBase)
            return task_prep_answer
        except openai.APIConnectionError as e:
            logger.error("The server could not be reached")
            logger.error(e.__cause__)
        except openai.RateLimitError as e:
            logger.error("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            logger.error("Another non-200-range status code was received")
            logger.error(e.status_code)
            logger.error(e.response)

    def _create_task_prep_prompt(
        self, flow: Flow, flow_run: FlowRun, task_operation_index: int, task_definition: TaskDefinition
    ) -> TaskPrepPromptBase:
        """
        Creates a task preparation prompt based on the given flow, flow run, task operation index, and task definition.

        Args:
            flow (Flow): The flow object representing the desired overarching flow.
            flow_run (FlowRun): The flow run object associated with the flow.
            task_operation_index (int): The index of the task operation within the flow context.
            task_definition (TaskDefinition): The task definition object representing the task to be executed.

        Returns:
            TaskPrepPromptBase: The task preparation prompt containing system and user messages.

        """

        task_operation = self._get_task_operation_by_index(flow, task_operation_index)

        messages = [
            {
                "role": "system",
                "content": """
                    You are part of an application that enables its users to automate tasks in a complex flow. 
                    
                    The user will give you a natural language request describing the desired overarching flow to be completed. 
                    For this request, a "soft flow" has been generated already.
                    The user will also give you this flow object of TaskOperations and Dependencies between these Task Operations, which
                    are annotated by natural language. The TaskOperations are sorted in the order they should be executed.
                    
                    These task operations point at task definitions that are actually Python methods in our codebase. You can think of them as
                    the actual tasks that need to be executed. The task definitions are defined in the database and have a unique identifier.
                    
                    The task operations are bascially an instance of a task definition within a flow context.
                    
                    Finally you will receive outputs from previous Task Operations that were executed before, in the form of
                    JSON outputs. You will receive the TaskDefinition model that also includes the input parameters; some of them
                    mandatory and some of them optional.
                    
                    Your task will be to format the parameters for the next task operation in the execution stack, based on the
                    given request, previous outputs and the upcoming task definition that needs to be executed in the task operation. Usually this will
                    take the form of looking at previous outputs and fetching an id, or applying some logic based on the request.
                    
                    
                    A Flow is defined as follows:
                    Flow(
                        task_operations=[TaskOperationBase(...), ...],
                        dependencies=[Dependency(...), ...],
                    )
                    
                    TaskOperationBase is defined as follows:
                    TaskOperationBase(
                        name="[TASK OPERATION NAME]",
                        task_definition="[TASK ID]",
                        instruction="[OPTIONAL USER PROVIDED ADDITIONAL INSTRUCTIONS]",
                        index=[UNIQUE INTEGER IDENTIFIER OF TASK OPERATION WITHIN FLOW CONTEXT],
                        sorted_index=[POSITION OF TASK OPERATION IN THE FLOW],
                    )
                    
                    Dependency is defined as follows:
                    Dependency(
                        instruction = string,
                        source_task_operation = int,
                        target_task_operation = int,
                    }
                    
                    TaskDefinition is defined as follows:
                    TaskDefinition(
                        task_name="Example Task", # task definition name
                        integration="123e4567-e89b-12d3-a456-426614174000", # unique identified
                        parameters=[TaskParameter(...)],  # List of TaskParameter instances
                        input_type="json",
                        input_yml="...",
                        description="This is an example task demonstrating how to define a task.",
                        python_method_name="example_task_method",
                        output_type="xml",
                        output_yml="...",
                    )
                    
                    TaskParameter is defined as follows:
                    TaskParameter(
                        name="...", # string
                        data_type="...", # string
                        position=..., # int
                        doc_string="...", # string
                        optional=bool
                    )
                    
                    TaskOutput is defined as follows:
                    TaskOutput(
                        task_operation_index=int,
                        output="...",
                    )
                    
                    You will give a list of small JSONs, each with depth 0, that map the name of the TaskParameter and the value that we must put in.
                    For your own context, we will use this to then call the TaskDefinition from our own codebase using the value that you specified.
                    The parameter will likely be directly pulled from the earlier outputs (like a name or id, with in some cases a small string or arithmetic operation ) 
                    or the request but don't have to necessarily. It may also be indirectly based on your intuition that you deem logical.
                    The list may also be empty, in case the task definition has no mandatory parameters.
                    
                    [
                        {
                            "name": <name of the task parameter of the task definition>,
                            "value": <the value that we must put in the parameter of this task definition>,
                            "explanation": <optional, an explanation why we are doing this. Also explain if you applied mental arithmetic or string operation here.>
                        },
                        ...
                        {
                            "name": <name of the task parameter of the task definition>,
                            "value": <the value that we must put in the parameter of this task definition>,
                            "explanation": <optional, an explanation why we are doing this. Also explain if you applied mental arithmetic or string operation here.>
                        },
                    ]
                """,
            },
            {
                "role": "user",
                "content": f"""
                    Request: find and update the project planning card by adding the following item: "migrate database"

                    This is task operation {task_operation_index} in the flow with name {task_operation.name}. In the sorted order this is number {task_operation.sorted_index} in the flow.
                    
                    Flow: {flow.model_dump()}
                    
                    Task Operation: {task_operation.model_dump()}
                    
                    Task Definition: {task_definition.model_dump()}
                    
                    Previous outputs: 
                    
                    {self._get_task_outputs_formatted_string(flow, flow_run)}
                    """,
            },
        ]

        return TaskPrepPromptBase(messages=messages)

    def _get_task_operation_by_index(self, flow: Flow, task_operation_index: int) -> TaskOperationBase:
        """
        Retrieves a task operation by its index.
        """

        task_operation = [task_op for task_op in flow.task_operations if task_op.index == task_operation_index]

        return task_operation[0]

    def _get_task_outputs_formatted_string(self, flow: Flow, flow_run: FlowRun) -> str:
        """
        Returns a formatted string of the task outputs.
        """
        formatted_outputs = []
        for task_run in flow_run.task_runs:
            formatted_outputs.append(
                f"Task operation with index {task_run.task_operation_index} and name {self._get_task_operation_by_index(flow, task_operation_index=task_run.task_operation_index)}: {str(task_run.result)}"
            )

        return "\n".join(formatted_outputs)


task_preparation_generator = TaskPreparationGenerator()
