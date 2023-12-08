from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.datetime_parse import date

from .task_operation import TaskOperationBase


# Shared properties
class FlowBase(BaseModel):
    flow_request: UUID
    name: Optional[str]
    task_operations: list[TaskOperationBase]
    

# Properties to receive via API on creation
class FlowCreate(FlowBase):
    created_by_human: bool = True
    modified_by_human: bool = True
    pass

# Properties to receive via API on update
class FlowUpdate(FlowCreate):
    pass


class FlowInDBBase(FlowBase):
    id: UUID
    created_date: datetime
    modified_date: datetime
    created_by_email: EmailStr
    modified_by_email: EmailStr
    
    class Config:
        orm_mode = True


# Additional properties to return via API
class Flow(FlowInDBBase):
    pass


# Additional properties stored in DB
class FlowInDB(FlowInDBBase):
    pass