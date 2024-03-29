from datetime import datetime
from typing import List, Optional
from uuid import UUID
from app.models import IntegrationCredential
from app.schemas import IntegrationCredentialCreate, IntegrationCredentialUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.models.integration import Integration


class CRUDIntegrationCredential(
    CRUDBase[IntegrationCredential, IntegrationCredentialCreate, IntegrationCredentialUpdate]
):

    def get_by_integration_and_user_email(
        self, db: Session, integration_id: UUID, modified_by_email: str
    ) -> Optional[IntegrationCredential]:
        """
        Get integration credential by integration id and user email.
        """

        return (
            db.query(self.model)
            .filter(self.model.integration == integration_id, self.model.modified_by_email == modified_by_email)
            .first()
        )
        
    def get_by_integration_short_name_and_user_email(self,
        db: Session, integration_short_name: str, modified_by_email: str
    ) -> Optional[IntegrationCredential]:
        """
        Get integration credential by integration short name and user email.
        """
        return (
            db.query(IntegrationCredential)
            .join(IntegrationCredential.credential_of)  # Join with the Integration model via credential_of relationship
            .filter(
                Integration.short_name == integration_short_name,  # Filter by short_name of the Integration
                IntegrationCredential.modified_by_email == modified_by_email  # and by modified_by_email
            )
            .first()
        )
        
    def update_by_integration_and_user_email(
        self, db: Session, modified_by_email: str, credential_update: IntegrationCredentialUpdate
    ) -> Optional[IntegrationCredential]:
        """
        Update integration credential by integration id and user email.
        """

        credential = self.get_by_integration_and_user_email(db, credential_update.integration, modified_by_email)
        if credential:
            credential.modified_by_email = modified_by_email
            credential.modified_date = datetime.utcnow()
            for key, value in credential_update.dict(exclude_unset=True).items():
                setattr(credential, key, value)
            db.commit()
            db.refresh(credential)
        return credential
    
    
    def get_all_for_user(self, db: Session, modified_by_email: str) -> List[IntegrationCredential]:
        """
        Get all integration credentials for a user.
        """

        return db.query(self.model).filter(self.model.modified_by_email == modified_by_email).all()


integration_credential = CRUDIntegrationCredential(IntegrationCredential)
