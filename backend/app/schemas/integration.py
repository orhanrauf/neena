from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class IntegrationBase(BaseModel):
    name: str
    short_name: str
    uses_api_key: bool
    uses_sso_key: Optional[bool] = False

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

    class Config:
        orm_mode = True

# Additional properties to return via API
class Integration(IntegrationInDBBase):
    pass

# Additional properties stored in DB
class IntegrationInDB(IntegrationInDBBase):
    pass