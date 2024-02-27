import instructor
import openai

from app.core.config import Settings
from app.db.session import SessionLocal
from app.schemas.task_prep_prompt import TaskPrepPromptBase
from app.schemas.flow import Flow
from app.schemas.flow_run import FlowRun
from app.schemas.task_definition import TaskDefinition


class TaskPreparationGenerator:
    """
    This class is responsible for preparing the parameters for a TaskOperation
    given the state Flow execution, Flow graph and previous TaskOperation outputs.
    """

    def __init__(
        self,
        openai_api_key: str = Settings.OPENAI_API_KEY,
        model: str = "gpt-4",
    ) -> None:
        self.model = model
        self.client = instructor.patch(openai.OpenAI(api_key=openai_api_key))
        self.database = SessionLocal()

    def _create_task_prep_prompt(
        self, flow: Flow, flow_run: FlowRun, task_operation_index: int, task_definition: TaskDefinition
    ) -> TaskPrepPromptBase:

        messages = [
            
                "role": "system",
                "content": """
                    You are part of an application that enables its users to automate complex tasks in Trello. 
                    
                    The user will give you a natural language request describing the desired overarching flow to be completed. 
                    The user will also give you a flow of TaskOperations and Dependencies between these Task Operations, which
                    are annotated by natural language.
                    These task operations point at task definitions that are actually Python methods in our codebase.
                    
                    Finally you will receive outputs from previous Task Operations that were executed before, in the form of
                    JSON outputs. You will receive the TaskDefinition model that also includes the input parameters; some of them
                    mandatory and some of them optional.
                    
                    
                    Your task will be to format the parameters for the next task operation in the execution stack, based on the
                    given request, previous outputs and the upcoming task definition that needs to be executed in the task operation. Usually this will
                    take the form of looking at previous outputs and fetching an id, or applying some logic based on the request.
                    
                    TaskOperationBase is defined as follows:
                    TaskOperationBase(
                        name="[TASK OPERATION NAME]",
                        task_definition="[TASK ID]",
                        instruction="[OPTIONAL USER PROVIDED ADDITIONAL INSTRUCTIONS]",
                        index=[UNIQUE INTEGER IDENTIFIER OF TASK OPERATION],
                    )
                    
                    TaskDefinition is defined as follows:
                    TaskDefinition(
                        task_name="[TASK DEFINITION NAME]",
                        integration="[UNIQUE IDENTIFIER]",
                        
                    )
                    
                    TaskDefinition(
                        task_name="Example Task", # task definition name
                        integration="123e4567-e89b-12d3-a456-426614174000", # unique identified
                        parameters=[...],  # List of TaskParameter instances
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
                    
                    You will give list of small JSONs, each with depth 0, that map the name of the TaskParameter and the value that we must put in.
                    For your own context, we will use this to then call the TaskDefinition from our own codebase using the value that you specified.
                    The parameter will likely be directly pulled from the earlier outputs (like a name or id, with in some cases a small string or arithmetic operation ) 
                    or the request but don't have to necessarily. It may also be indirectly based on your intuition that you deem logical.
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
            ,
            {
                "role": "user",
                "content": """
                    Request: find and update the project planning card by adding the following item: "migrate database"

                    Flow: task_operations: {
                        ""
                    }
                
                
                
                
                """,
            },
        ]
