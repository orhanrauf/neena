from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.datetime_parse import date


class Argument(BaseModel):
    name: str
    source: str
    value: str
    data_type: str
    nullable: bool

    class Config:
        orm_mode = True


# Shared properties
class TaskOperationBase(BaseModel):
    name: str
    task_definition: UUID
    arguments: list[Argument]
    explanation: Optional[str] = None
    x: float
    y: float
    z: int

    class Config:
        orm_mode = True
    
# Properties to receive via API on creation
class TaskOperationCreate(TaskOperationBase):
    flow: UUID
    pass


# Properties to receive via API on update
class TaskOperationUpdate(TaskOperationCreate):
    pass


class TaskOperationInDBBase(TaskOperationBase):
    id: UUID
    flow: UUID
    
    created_date: datetime
    modified_date: datetime
    created_by_email: EmailStr
    modified_by_email: EmailStr


# Additional properties to return via API
class TaskOperation(TaskOperationInDBBase):
    pass


# Additional properties stored in DB
class TaskOperationInDB(TaskOperationInDBBase):
    pass
