"""
This file contains a template for a local script that can be used to interact with the backend code.
"""

import sys
import os
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app import crud
from app.flow_execution.core import ExecutionContext

from app.schemas.task_definition import TaskDefinition, TaskDefinitionBase
from app.schemas.flow import FlowBase
from app.schemas.task_operation import TaskOperationBase
from app.flow_execution.integrations.trello import TrelloIntegration
from app.flow_execution.models.trello import (
    TrelloBoard,
    TrelloBoardCreate,
    TrelloBoardGet,
    TrelloBoardUpdate,
    TrelloCard,
    TrelloCardCreate,
    TrelloList,
    TrelloListCreate,
    TrelloListsInBoardGet,
)


# Assuming your .env file is in the current directory or specify the path
dotenv_path = "../../.env"

# Load or reload the .env file
load_dotenv(dotenv_path=dotenv_path)

# Add the backend directory to the sys.path to allow for absolute imports
sys.path.append(os.path.abspath("."))

from app.core.config import settings

db = SessionLocal()

user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

execution_context = ExecutionContext(user)

integration = execution_context.get_integration_instance("3eb7db14-a852-4b22-a17f-d408a53d2bc6")

boards = integration.get_boards()

board = TrelloBoard(**boards.data[0])


# trello_integration_class = TrelloIntegration(user)


# list_create = TrelloListCreate(name="Test List", id_board=board.id, pos="top")

# created_list_task_respose = trello_integration_class.create_list(list_create)

# created_list = created_list_task_respose.data


# create_card = TrelloCardCreate(name="Test Card", id_list=created_list.id, desc="Dit is een test card", pos="top")
# created_card = trello_integration_class.create_card(create_card)

# print(created_card.data)
