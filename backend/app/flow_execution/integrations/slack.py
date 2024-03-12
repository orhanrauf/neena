from typing import Any

from app import schemas
from app.core.config import settings
from app.core.secrets import secrets_service
from app.flow_execution.integrations.base import BaseIntegration
from app.flow_execution.decorators import integration, task

from app.flow_execution.models.slack import SlackBase, SlackBaseUpdate


@integration(name="Slack", short_name="slack")
class SlackIntegration(BaseIntegration):
    """
    Integration class for Slack.
    Models implemented: TODO.
    """

    key: str
    token: str

    def __init__(self, user: schemas.User) -> None:
        # TODO: self.key = settings.SLACK_API_KEY
        self.user = user

    def _fetch_credentials(self) -> str:
        """
        Fetches the user-specific Slack token from the key vault.
        """
        return secrets_service.get_secret(self.user, self._short_name)
