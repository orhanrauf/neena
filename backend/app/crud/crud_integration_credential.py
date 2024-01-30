from app.models.integration_credential import IntegrationCredential
from app.schemas import IntegrationCredentialCreate, IntegrationCredentialUpdate
from app.crud.base import CRUDBase

class CRUDIntegrationCredential(CRUDBase[IntegrationCredential, IntegrationCredentialCreate, IntegrationCredentialUpdate]):
    pass

integration_credential = CRUDIntegrationCredential(IntegrationCredential)
