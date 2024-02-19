from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Shared properties
class IntegrationCredentialBase(BaseModel):
    integration: UUID

# Properties to receive via API on creation
class IntegrationCredentialCreate(IntegrationCredentialBase):
    credential: str
    

# Properties to receive via API on update
class IntegrationCredentialUpdate(IntegrationCredentialBase):
    credential: str

class IntegrationCredentialInDBBase(IntegrationCredentialBase):
    id: Optional[UUID] = None
    integration: UUID
    created_by_email: EmailStr
    organization: Optional[UUID] = None
    modified_by_email: EmailStr
    created_date: datetime
    modified_date: datetime

    class Config:
        orm_mode = True

# Additional properties to return via API
class IntegrationCredential(IntegrationCredentialInDBBase):
    pass

# Additional properties stored in DB
class IntegrationCredentialInDB(IntegrationCredentialInDBBase):
    pass

class IntegrationCredentialInKeyVault(IntegrationCredentialCreate, IntegrationCredentialInDBBase):
    pass
    