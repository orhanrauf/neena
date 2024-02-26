import openai

from typing import Any
from openai.types.chat.chat_completion import ChatCompletion
from app.schemas.flow import FlowBase
from app.schemas.task_definition import TaskDefinitionBase

class FlowGenerator:
    """
    Class that accepts user request, and generates and returns porperply 
    formatted flow for execution layer.
    """
    def __init__(self) -> None:
        # init stuff like the openai client, model type,
        pass
    
    def generate_flow_from_request(self, request: str) -> FlowBase:
        """Main entry point of class"""
        pass
    
    def get_requested_task_definitions_from_database(self) -> list[TaskDefinitionBase]:
        # Consider moving this to its own class; 
        # e.g., TaskDefinitionRetriever, TaskDefinitionGetter
        pass
    
    def method_that_organizes_task_definitions_into_flow(self) -> list[TaskDefinitionBase]:
        pass
    
    