import requests

from typing import Any

from app.flow_execution.decorators import integration, task
from app.flow_execution.integrations.base import BaseIntegration
from app import schemas
from slack_sdk import WebClient
from slack_sdk.web.base_client import SlackResponse
from app.core.secrets import secrets_service
from app.core.config import settings
from app.flow_execution.decorators import task
from app.flow_execution.models.slack import SlackChat, SlackConversation


@integration(name="Slack", short_name="slack")
class SlackIntegration(BaseIntegration):
    """
    Integration class for Slack.
    Models implemented: message.
    """

    key: str
    token: str

    def __init__(self, user: schemas.User) -> None:
        self.key = settings.SLACK_APP_ID
        self.user = user
        self.token = self._fetch_credentials()

        self.base_url = self._construct_base_url()
        self.headers = self._construct_headers()
        self.base_params = self._construct_base_params()
        self.client = WebClient(token=self.token)

    def _fetch_credentials(self) -> str:
        """
        Fetches the user-specific Slack token from the key vault.
        """
        return NotImplementedError

    def check_connectivity(self) -> bool:
        """
        Checks if the Slack API is accessible and the SDK is working.
        """

        return NotImplementedError

    def _construct_base_url(self) -> str:
        """
        Constructs the base URL for the Slack API.
        """
        return NotImplementedError

    def _construct_headers(self) -> Any:
        return NotImplementedError

    @task(task_name="Send Message")
    def send_message(self, message: Any):
        # def send_message(self, message: SlackBase) -> SlackBase:
        """
        Sends a message to a Slack channel.
        """
        response = self.client.chat_postMessage(channel=message.channel, text=message.text)
        return message
