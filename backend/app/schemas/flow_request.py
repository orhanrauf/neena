from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


# Shared properties
class FlowRequestBase(BaseModel):
    request_metadata: Optional[List[Dict]] = None
    request_instructions: constr(min_length=8, max_length=512)
    request_name: Optional[constr(max_length=64)] = None
    flow: Optional[UUID] = None
    organization: Optional[UUID] = None

# Properties to receive via API on creation
class FlowRequestCreate(FlowRequestBase):
    pass

# Properties to receive via API on update
class FlowRequestUpdate(FlowRequestCreate):
    pass


class FlowRequestInDBBase(FlowRequestBase):
    id: Optional[UUID] = None
    created_date: datetime
    modified_date: datetime
    created_by_email: EmailStr
    modified_by_email: EmailStr
    
    class Config:
        from_attributes = True


# Additional properties to return via API
class FlowRequest(FlowRequestInDBBase):
    pass


# Additional properties stored in DB
class FlowRequestInDB(FlowRequestInDBBase):
    pass
