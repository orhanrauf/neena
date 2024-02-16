from core.keyvault import key_vault
from core.config import settings


class BaseIntegration:
    """
    Base class for integration implementations.
    """

    def fetch_credentials(self) -> dict:
        """
        Fetch the credentials for the integration.
        """
        raise NotImplementedError
    
    def check_connectivity() -> bool:
        """
        Check if the integration is reachable.
        """
        raise NotImplementedError
    
        
