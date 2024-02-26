from sqlalchemy.orm import Session
from uuid import UUID
from app.models.integration import Integration
from app.schemas import IntegrationCreate, IntegrationUpdate
from app.crud.base import CRUDBase

class CRUDIntegration(CRUDBase[Integration, IntegrationCreate, IntegrationUpdate]):
    def get_by_short_name(self, db: Session, short_name: str) -> Integration:
        return db.query(self.model).filter(self.model.short_name == short_name).first()
    
    def get_or_create_integration(self, db: Session, integration_create: IntegrationCreate) -> UUID:
        # Check if an integration with the given short_name already exists
        integration = self.get_by_short_name(db, integration_create.short_name)
        if integration:
            return integration.id  # Return the existing integration's UUID
        
        # If not found, create a new integration
        integration_data = integration_create.model_dump()  # Assuming IntegrationCreate is a Pydantic model
        new_integration = Integration(**integration_data)
        db.add(new_integration)
        db.commit()
        db.refresh(new_integration)  # Refresh to retrieve the generated UUID
        return new_integration.id

integration = CRUDIntegration(Integration)
