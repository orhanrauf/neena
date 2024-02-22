from typing import Any, List
import requests
from app.flow_execution.integrations.base import BaseIntegration
from app.flow_execution.decorators import integration, task

from app import schemas
from app.core.config import settings
from app.core.secrets import secrets_service

from app.flow_execution.models.trello import (
    TrelloCard,
    TrelloCardCreate,
    TrelloCardGet,
    TrelloCardUpdate,
    TrelloCardDelete,
    TrelloList,
    TrelloListCreate,
    TrelloListGet,
    TrelloListUpdate,
    TrelloBoard,
    TrelloBoardCreate,
    TrelloBoardGet,
    TrelloBoardUpdate,
    TrelloBoardDelete
)

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
        self.token = self._fetch_credentials()
        

        self.base_url = self._construct_base_url()    
        self.headers = self._construct_headers()
        self.base_params = self._construct_base_params()

    def _fetch_credentials(self) -> str:
        """
        Fetches the user-specific Trello token from the key vault.
        """
        return secrets_service.get_secret(self.user, self.short_name)
    
    def _construct_base_url(self) -> str:
        """
        Constructs the base URL for the Trello API.
        """
        return f"https://api.trello.com/1/"
    
    def _construct_headers(self) -> dict:
        """
        Constructs headers required for making requests to the Trello API.
        """
        return {
            "Content-Type": "application/json"
        }

    def _construct_base_params(self) -> dict:
        """
        Constructs the base query parameters for requests to the Trello API.
        """
        return {
            "key": self.key,
            "token": self.token
        }
    
    def check_connectivity(self) -> bool:
        """
        Checks if the Trello API is accessible.
        """
        
        url = f"{self.base_url}members/me/boards"
        
        response = requests.get(
            url=url,
            headers=self.headers,
            params=self.base_params
        )
        return response.status_code == 200
    
    @task('Get Boards')
    def get_boards(self) -> List[TrelloBoard]:
        """
        Fetches the boards for the user.
        """
        
        url = f"{self.base_url}members/me/boards"
        
        response = requests.get(
            url=url,
            headers=self.headers,
            params=self.base_params
        )
        return response.json()

    @task('Create Board')
    def create_board(self, board: TrelloBoardCreate) -> TrelloBoard:
        """
        Creates a new board.
        """
        
        url = f"{self.base_url}boards"
        
        response = requests.post(
            url=url,
            headers=self.headers,
            params=self.base_params,
            json=board.dict()
        )
        return response.json()
    
    
    
    
    