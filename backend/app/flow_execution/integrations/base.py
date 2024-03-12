from abc import ABC, abstractmethod
from typing import Any

from app import schemas

class BaseIntegration(ABC):
    """
    Abstract base class for integration implementations.
    """
    
    user: schemas.User
    
    @abstractmethod
    def check_connectivity(self) -> bool:
        """
        Check if the integration is reachable.
        """
        raise NotImplementedError
    
    @abstractmethod
    def _fetch_credentials(self) -> Any:
        """
        Fetch the credentials for the integration.
        """
        raise NotImplementedError
    
