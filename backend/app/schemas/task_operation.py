from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


# Shared properties
class TaskOperationBase(BaseModel):
    name: str
    task_definition: UUID
    instruction: Optional [str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    index: int
    sorted_index: Optional[int] = None

    class Config:
        from_attributes = True
        from_orm = True


# Properties to receive via API on creation
class TaskOperationCreate(TaskOperationBase):
    flow: UUID
    pass


# Properties to receive via API on update
class TaskOperationUpdate(TaskOperationBase):
    id: Optional[UUID] = None


class TaskOperationInDBBase(TaskOperationBase):
    id: UUID
    flow: UUID

    created_date: datetime
    modified_date: datetime
    created_by_email: EmailStr
    modified_by_email: EmailStr

    class Config:
        from_attributes = True
        from_orm = True


# Additional properties to return via API
class TaskOperation(TaskOperationInDBBase):
    pass


# Additional properties stored in DB
class TaskOperationInDB(TaskOperationInDBBase):
    pass
