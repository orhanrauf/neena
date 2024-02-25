from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class OrganizationBase(BaseModel):
    auth0_id: str

# Properties to receive via API on creation
class OrganizationCreate(OrganizationBase):
    pass

# Properties to receive via API on update
class OrganizationUpdate(OrganizationBase):
    auth0_id: Optional[str] = None

class OrganizationInDBBase(OrganizationBase):
    id: Optional[UUID] = None
    created_date: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class Organization(OrganizationInDBBase):
    pass

# Additional properties stored in DB
class OrganizationInDB(OrganizationInDBBase):
    pass
