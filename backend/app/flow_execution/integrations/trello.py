from typing import Any
from app.flow_execution.integrations.base import BaseIntegration
from app.flow_execution.decorators import integration, task

from app import schemas
from app.core.config import settings
from backend.app.core.secrets import key_vault
from app.crud import integration_credential


@integration
class TrelloIntegration(BaseIntegration):
    """
    Integration class for Trello. 
    Models implemented: boards, lists, and cards.
    """
    
    key: str
    token: str
    
    @property
    def name(self) -> str:
        return 'Trello'
    
    @property
    def short_name(self) -> str:
        return 'trello'
    
    def __init__(self, user: schemas.User):
        self.key = settings.TRELLO_API_KEY
        self.user = user
        self.token = self.fetch_credentials()

    def fetch_credentials(self) -> str:
        return
    
    def check_connectivity(self) -> bool:
        return
    
    @task(max_attempts=3, delay_seconds=2)
    def fetch_boards(self) -> list:
        # makes API call to Trello board for specific customer
        return
    
    
    
    