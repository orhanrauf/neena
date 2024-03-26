import os
import sys
import pdb

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.core.secrets import secrets_service

from app.db.session import SessionLocal
from app import crud
from app.core.config import settings

from app.flow_execution.integrations.slack import SlackIntegration
from app.flow_execution.models.slack import SlackChatMessage, SlackChatMessageSend


def main() -> None:

    ### Simple chat message sending tests ###
    # client = WebClient(token=os.environ["SLACK_OAUTH_TOKEN"])
    # try:
    #     # response = client.chat_postMessage(channel="#random", text="Seh ruman")
    #     response = client.conversations_create(name="gewoon-ff-teste-tog")
    #     print(f"full response: {response}")
    #     # print(response["message"])
    #     # assert response["message"]["text"] == "Seh ruman"
    # except SlackApiError as e:
    #     # You will get a SlackApiError if "ok" is False
    #     assert e.response["ok"] is False
    #     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    #     print(f"Got an error: {e.response['error']}")
    #     # Also receive a corresponding status_code
    #     assert isinstance(e.response.status_code, int)
    #     print(f"Received a response status_code: {e.response.status_code}")
    #########################################

    ### SlackIntegration tests ###
    # Assuming your .env file is in the current directory or specify the path
    dotenv_path = "../../.env"

    # Load or reload the .env file
    load_dotenv(dotenv_path=dotenv_path)

    db = SessionLocal()
    HARDCODED_EMAIL = "lennert@neena.io"
    user = crud.user.get_by_email(db, email=HARDCODED_EMAIL)

    slack_integration = SlackIntegration(user)

    # test message #
    # response = slack_integration.client.chat_postMessage(channel="#random", text="Dit is een test.")
    # print(response["message"])
    # assert response["message"]["text"] == "Dit is een test."
    ################

    # check connectivity #
    connected = slack_integration.check_connectivity()
    print(f"Connected: {connected}")

    slack_chat_send_message = SlackChatMessageSend(channel="#random", text="We are so back, baby.")
    response = slack_integration.send_message(message_to_send=slack_chat_send_message)
    print(response.data["message"])
    assert response.data["message"]["text"] == "We are so back, baby."


if __name__ == "__main__":
    main()
