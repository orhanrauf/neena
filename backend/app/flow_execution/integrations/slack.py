import os
import requests

from typing import Any

from app.flow_execution.decorators import integration, task
from app.flow_execution.integrations.base import BaseIntegration
from app.flow_execution.models.base import BaseIntegrationActionModel
from app import schemas
from slack_sdk import WebClient
from slack_sdk.web.base_client import SlackResponse
from app.core.secrets import secrets_service
from app.core.config import settings
from app.flow_execution.decorators import task
from app.flow_execution.models.slack import (
    SlackChatMessage,
    SlackChatMessageSend,
    SlackChatMessageDelete,
    SlackChatMessageUpdate,
)


@integration(name="Slack", short_name="slack")
class SlackIntegration(BaseIntegration):
    """
    Integration class for Slack.
    Models implemented: message.
    """

    key: str
    token: str

    def __init__(self, user: schemas.User) -> None:
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
        return secrets_service.get_secret(self.user, self._short_name)

    def _construct_headers(self) -> dict:
        """
        Constructs headers required for making requests to the Slack API.
        """
        return {"Content-Type": "application/json"}

    def _construct_base_url(self) -> str:
        """
        Constructs the base URL for the Slack API.
        """
        return f"https://api.slack.com/"

    def _construct_base_params(self) -> dict:
        """
        Constructs the base query parameters for requests to the Slack API.
        """
        return {"key": self.key, "token": self.token}

    def _model_to_query_params(self, model: BaseIntegrationActionModel) -> dict[str, Any]:
        """
        Converts a Pydantic model instance into a dictionary suitable for query parameters,
        respecting field aliases.
        """
        model_dict = model.model_dump(by_alias=True, exclude_none=True)
        return {**self.base_params, **model_dict}

    def check_connectivity(self) -> bool:
        """
        Checks if the Slack API is accessible and the SDK is working.
        """

        url = f"{self.base_url}methods/"

        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return response.status_code == 200

    @task(task_name="Send Message")
    def send_message(self, message_to_send: SlackChatMessageSend) -> Any:
        """
        Sends a message to a Slack channel.
        """
        params = self._model_to_query_params(message_to_send)
        return self.client.chat_postMessage(**params)

    @task(task_name="Update Message")
    def update_message(self, message_to_update: SlackChatMessageUpdate) -> Any:
        """
        Updates a message in a Slack channel.
        """
        params = self._model_to_query_params(message_to_update)
        return self.client.chat_update(**params)

    @task(task_name="Delete Message")
    def delete_message(self, message_to_delete: SlackChatMessageDelete) -> Any:
        """
        Deletes a message in a Slack channel.
        """
        params = self._model_to_query_params(message_to_delete)
        return self.client.chat_delete(**params)
