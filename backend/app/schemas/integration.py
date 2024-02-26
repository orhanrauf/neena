from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class IntegrationBase(BaseModel):
    class_name: str
    name: str
    short_name: str
    
# Properties to receive via API on creation
class IntegrationCreate(IntegrationBase):
    pass

# Properties to receive via API on update
class IntegrationUpdate(IntegrationBase):
    name: Optional[str] = None
    short_name: Optional[str] = None
    uses_api_key: Optional[bool] = None
    uses_sso_key: Optional[bool] = None

class IntegrationInDBBase(IntegrationBase):
    id: Optional[UUID] = None
    created_date: datetime
    modified_date: datetime
    uses_api_key: Optional[bool] = None
    uses_sso_key: Optional[bool] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Integration(IntegrationInDBBase):
    pass

# Additional properties stored in DB
class IntegrationInDB(IntegrationInDBBase):
    pass