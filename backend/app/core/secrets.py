from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.core.config import settings

from app.db.session import SessionLocal
from app import crud
from app.schemas.user import User

class AzureKeyVault:
    def __init__(self):
        self.vault_url = f"https://{settings.AZURE_KEYVAULT_NAME}.vault.azure.net/"
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a secret from Azure Key Vault.

        :param secret_name: The name of the secret to retrieve.
        :return: The value of the secret.
        """
        secret = self.client.get_secret(secret_name)
        return secret.value
    
    def set_secret(self, secret_name: str, secret_value: str) -> None:
        """
        Sets a secret in Azure Key Vault.

        :param secret_name: The name of the secret to set.
        :param secret_value: The value of the secret.
        """
        self.client.set_secret(secret_name, secret_value)

key_vault = AzureKeyVault()


class IntegrationSecretsService:
    """
    Service class for retrieving secrets for enabled integrations of a user.
    """
    def __init__(self):
        self.key_vault = key_vault
        self.db = SessionLocal()
        
    def get_secret(self, user: User, integration_short_name: str) -> str:
        """
        Retrieves a secret from Azure Key Vault based on the user email and integration short name.

        :param user_email: The email of the user.
        :param integration_short_name: The short name of the integration.
        
        :return: The value of the secret.
        """
        
        integration_credential = crud.integration_credential.get_by_integration_short_name_and_user_email(self.db, integration_short_name, user.email)
        
        return key_vault.get_secret(integration_credential.id)


secrets_service = IntegrationSecretsService()