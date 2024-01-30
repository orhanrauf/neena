from app.models.integration import Integration
from app.schemas import IntegrationCreate, IntegrationUpdate
from app.crud.base import CRUDBase

class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationUpdate]):
    pass

integration = CRUDIntegration(Integration)
