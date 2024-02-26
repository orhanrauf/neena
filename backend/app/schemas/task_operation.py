from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


# Shared properties
class TaskOperationBase(BaseModel):
    name: str
    task_definition: UUID
    instruction: str
    x: Optional[float] = None
    y: Optional[float] = None
    index: int

    class Config:
        from_attributes = True


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
