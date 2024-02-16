from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.core.config import settings

class AzureKeyVault:
    def __init__(self):
        self.vault_url = f"https://{settings.KEY_VAULT_NAME}.vault.azure.net/"
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