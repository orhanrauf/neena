import openai

from typing import Any
from fastapi import Depends
from sqlalchemy.orm import Session
from openai.types.chat.chat_completion import ChatCompletion

from app.core.config import settings
from app.schemas.flow import FlowBase
from app.schemas.task_definition import TaskDefinition
from app.schemas.task_operation import TaskOperationBase
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
        # TODO: consolidate OpenAI config stuff into its own class
        # idem for:
        # #### prompt handling
        # #### ...
        self.model = model
        self.client = openai.OpenAI(api_key=openai_api_key)
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
        return self.generate_flow_from_requested_task_operations(
            request=request, requested_task_operations=task_operations
        )

    def get_requested_task_definitions_from_database(self, request: str) -> list[TaskDefinition]:
        # Consider moving this to its own class;
        # e.g., TaskDefinitionRetriever, TaskDefinitionGetter
        # TODO: This is where eventually the RAG happens:
        # #### This method (later will become a class) interprets the request using RAG (i.e., 1 API call)
        # #### so it knows which TaskDefinitions it can and should get from the database
        requested_task_definitions = ["Get Boards", "Get List", "Get Card", "Update Card"]
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
                    You must return a list of dependencies in the following form:
                    dependencies = [
                        DependencyBase(instruction="[OPTIONAL INSTRUCTION ABOUT DEPENDENCY 0]", source_task_operation=[SOURCE TASK OPERATION INDEX], target_task_operation=[SOURCE TASK OPERATION INDEX]),
                        ...,
                        DependencyBase(instruction="[OPTIONAL INSTRUCTION ABOUT DEPENDENCY N]", source_task_operation=[SOURCE TASK OPERATION INDEX], target_task_operation=[SOURCE TASK OPERATION INDEX]),
                    ]
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
        print(f"TASK OPERATIONS: {requested_task_operations}")
        chat_completion = self._create_chat_completion_for_messages(messages)
        return self._extract_last_message_from_chat_completion(chat_completion)

    def _create_chat_completion_for_messages(self, messages: list) -> ChatCompletion:
        try:
            chat_completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return chat_completion
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


flow_generator = FlowGenerator()

# find update the project planning card by adding the following item: "migrate database"
# Get Board, Get List, Update Card
