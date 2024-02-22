from abc import ABC, abstractmethod
from typing import Any

from app import schemas

class BaseIntegration(ABC):
    """
    Abstract base class for integration implementations.
    """
    
    user: schemas.User
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the integration.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def short_name(self) -> str:
        """
        A short, unique name for the integration.
        """
        raise NotImplementedError
    
    @abstractmethod
    def check_connectivity() -> bool:
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
        
