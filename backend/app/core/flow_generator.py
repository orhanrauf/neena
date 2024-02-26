import openai

from typing import Any
from fastapi import Depends
from sqlalchemy.orm import Session
from openai.types.chat.chat_completion import ChatCompletion

from app.core.config import settings
from app.schemas.flow import FlowBase
from app.schemas.task_definition import TaskDefinitionBase
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
        # init stuff like the openai client, model type,
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
        # [DUMMY STEP] collection of TaskDefinitionBase's = self.from_request_determine_task_definitions_using_rag(request) / Communicates with database / TaskDefinitionGetter (API Call 1)
        task_definitions = self.get_requested_task_definitions_from_database(request)
        # flow = self.generate_flow_from_requested_task_definitions(request, task_definitions)
        # flow = self.generate_flow_from_request_given_task_definitions(request, list[TaskDefinitionBase]) (API Call 2)
        # return flow
        return task_definitions

    def get_requested_task_definitions_from_database(self, request: str) -> list[TaskDefinitionBase]:
        # Consider moving this to its own class;
        # e.g., TaskDefinitionRetriever, TaskDefinitionGetter
        # TODO: This is where eventually the RAG happens:
        # #### This method (later will become a class) interprets the request using RAG (i.e., 1 API call)
        # #### so it knows which TaskDefinitions it can and should get from the database
        return task_definition.get_multi(db=self.database)

    def generate_flow_from_requested_task_definitions(
        self, request: str, requested_task_definitons: list[TaskDefinitionBase]
    ) -> Any:
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant, skilled in explaining solutions in simple yet effective language.",
            },
            {"role": "user", "content": request},
        ]
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
        return chat_completion

    #### COPIED FROM OpenAIService ####
    def get_response_to_request(self, request: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant, skilled in explaining solutions in simple yet effective language.",
            },
            {"role": "user", "content": request},
        ]
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
        return chat_completion.choices[0].message.content + "FlowGenerator"

    #### End ####


flow_generator = FlowGenerator()
