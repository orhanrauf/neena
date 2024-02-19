from app.models.integration import Integration
from app.schemas import IntegrationCreate, IntegrationUpdate
from app.crud.base import CRUDBase

class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationUpdate]):
    def get_by_short_name(self, db, short_name: str) -> Integration:
        return db.query(self.model).filter(self.model.short_name == short_name).first()

integration = CRUDIntegration(Integration)
