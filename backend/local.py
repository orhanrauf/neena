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
from app.flow_execution.integrations.slack import SlackIntegration

from app.flow_execution.models.slack import SlackChatMessageSend


# Assuming your .env file is in the current directory or specify the path
dotenv_path = "../../.env"

# Load or reload the .env file
load_dotenv(dotenv_path=dotenv_path)

# Add the backend directory to the sys.path to allow for absolute imports
sys.path.append(os.path.abspath("."))

ssl_path = "/Users/raufakdemir/Documents/Neena AI/neena/backend/venv/lib/python3.10/site-packages/certifi/cacert.pem"
os.environ["SSL_CERT_FILE"] = ssl_path
os.environ["REQUESTS_CA_BUNDLE"] = ssl_path

from app.core.config import settings

db = SessionLocal()

user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

slack_integration_class = SlackIntegration(user)

message_to_send = SlackChatMessageSend(channel="general", text="Test message")

response = slack_integration_class.send_message(message_to_send=message_to_send)

print(response)

# trello_integration_class = TrelloIntegration(user)


# list_create = TrelloListCreate(name="Test List", id_board=board.id, pos="top")

# created_list_task_respose = trello_integration_class.create_list(list_create)

# created_list = created_list_task_respose.data


# create_card = TrelloCardCreate(name="Test Card", id_list=created_list.id, desc="Dit is een test card", pos="top")
# created_card = trello_integration_class.create_card(create_card)

# print(created_card.data)
