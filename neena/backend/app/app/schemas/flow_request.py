from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, datetime_parse
from pydantic.datetime_parse import date


# Shared properties
class FlowRequestBase(BaseModel):
    request_metadata: list[dict] = []
    request_instructions : constr(max_length=512) = None
    request_body: constr(min_length=8, max_length=512)

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
        orm_mode = True


# Additional properties to return via API
class FlowRequest(FlowRequestInDBBase):
    pass


# Additional properties stored in DB
class FlowRequestInDB(FlowRequestInDBBase):
    pass
