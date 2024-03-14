from typing import Any, Dict, List
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
    TrelloCardsInListGet,
    TrelloBoard,
    TrelloBoardCreate,
    TrelloBoardGet,
    TrelloBoardUpdate,
    TrelloBoardDelete,
    TrelloListsInBoardGet,
)
from app.flow_execution.models.base import BaseIntegrationActionModel


@integration(name="Trello", short_name="trello")
class TrelloIntegration(BaseIntegration):
    """
    Integration class for Trello.
    Models implemented: boards, lists, and cards.
    """

    key: str
    token: str

    def __init__(self, user: schemas.User) -> None:
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
        return secrets_service.get_secret(self.user, self._short_name)

    def _construct_base_url(self) -> str:
        """
        Constructs the base URL for the Trello API.
        """
        return f"https://api.trello.com/1/"

    def _construct_headers(self) -> dict:
        """
        Constructs headers required for making requests to the Trello API.
        """
        return {"Content-Type": "application/json"}

    def _construct_base_params(self) -> dict:
        """
        Constructs the base query parameters for requests to the Trello API.
        """
        return {"key": self.key, "token": self.token}

    def _model_to_query_params(self, model: BaseIntegrationActionModel) -> Dict[str, Any]:
        """
        Converts a Pydantic model instance into a dictionary suitable for query parameters,
        respecting field aliases.
        """
        model_dict = model.model_dump(by_alias=True, exclude_none=True)
        return {**self.base_params, **model_dict}

    def check_connectivity(self) -> bool:
        """
        Checks if the Trello API is accessible.
        """

        url = f"{self.base_url}members/me/boards"

        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return response.status_code == 200

    @task("Get Boards")
    def get_boards(self) -> List[TrelloBoard]:
        """
        Fetches the boards for the user.
        """

        url = f"{self.base_url}members/me/boards"

        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return response.json()

    @task("Create Board")
    def create_board(self, board: TrelloBoardCreate) -> TrelloBoard:
        """
        Creates a new board.
        """

        url = f"{self.base_url}boards"

        response = requests.post(url=url, headers=self.headers, params=self._model_to_query_params(board))
        return response.json()

    @task("Get Board")
    def get_board(self, board_get: TrelloBoardGet) -> TrelloBoard:
        """
        Fetches details of a specific board.
        """
        url = f"{self.base_url}boards/{board_get.id}"
        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return TrelloBoard(**response.json())

    @task("Update Board")
    def update_board(self, board_update: TrelloBoardUpdate) -> TrelloBoard:
        """
        Updates an existing board.
        """
        url = f"{self.base_url}boards/{board_update.id}"
        response = requests.put(url=url, headers=self.headers, params=self._model_to_query_params(board_update))
        return TrelloBoard(**response.json())

    @task("Delete Board")
    def delete_board(self, board_delete: TrelloBoardDelete) -> Any:
        """
        Deletes (or archives) an existing board.
        """
        url = f"{self.base_url}boards/{board_delete.id}"
        response = requests.put(url=url, headers=self.headers, params=self.base_params)
        return response.json()

    @task("Create Card")
    def create_card(self, card_create: TrelloCardCreate) -> TrelloCard:
        """
        Creates a new card.
        """
        url = f"{self.base_url}cards"
        response = requests.post(url=url, headers=self.headers, params=self._model_to_query_params(card_create))
        return TrelloCard(**response.json())

    @task("Get Card")
    def get_card(self, card_get: TrelloCardGet) -> TrelloCard:
        """
        Fetches details of a specific card.
        """
        url = f"{self.base_url}cards/{card_get.id}"
        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return TrelloCard(**response.json())

    @task("Update Card")
    def update_card(self, card_update: TrelloCardUpdate) -> TrelloCard:
        """
        Updates an existing card.
        """
        url = f"{self.base_url}cards/{card_update.id}"
        response = requests.put(url=url, headers=self.headers, params=self._model_to_query_params(card_update))
        return TrelloCard(**response.json())

    @task("Delete Card")
    def delete_card(self, card_delete: TrelloCardDelete) -> Any:
        """
        Deletes an existing card.
        """
        url = f"{self.base_url}cards/{card_delete.id}"
        response = requests.delete(url=url, headers=self.headers, params=self.base_params)
        return response.json()

    @task("Create List")
    def create_list(self, list_create: TrelloListCreate) -> TrelloList:
        """
        Creates a new list.
        """
        url = f"{self.base_url}lists"
        response = response = requests.post(
            url=url, headers=self.headers, params=self._model_to_query_params(list_create)
        )
        return TrelloList(**response.json())

    @task("Get List")
    def get_list(self, list_get: TrelloListGet) -> TrelloList:
        """
        Fetches details of a specific list.
        """
        url = f"{self.base_url}lists/{list_get.id}"
        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return TrelloList(**response.json())

    @task("Update List")
    def update_list(self, list_update: TrelloListUpdate) -> TrelloList:
        """
        Updates an existing list.
        """
        url = f"{self.base_url}lists/{list_update.id}"
        response = requests.put(url=url, headers=self.headers, params=self._model_to_query_params(list_update))
        return TrelloList(**response.json())

    @task("Get Cards in List")
    def get_cards_in_list(self, cards_in_list_get: TrelloCardsInListGet) -> List[TrelloCard]:
        """
        Fetches all cards in a specific list.
        """
        url = f"{self.base_url}lists/{cards_in_list_get.id}/cards"
        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return [TrelloCard(**card) for card in response.json()]

    # TODO: Fix typing on list return values
    @task("Get Lists in Board")
    def get_lists_in_board(self, lists_in_board_get: TrelloListsInBoardGet) -> List[TrelloList]:
        """
        Fetches all lists in a specific board.
        """
        url = f"{self.base_url}boards/{lists_in_board_get.id}/lists"
        response = requests.get(url=url, headers=self.headers, params=self.base_params)
        return [TrelloList(**list) for list in response.json()]
