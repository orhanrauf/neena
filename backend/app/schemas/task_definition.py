from datetime import datetime
from typing import Optional
from uuid import UUID
from app.core.shared_models import TaskParameter

from pydantic import BaseModel, EmailStr, constr


# Shared properties
class TaskDefinitionBase(BaseModel):
    task_name: constr(min_length=6, max_length=64)
    integration: UUID
    parameters: list[TaskParameter]
    input_type: str
    input_yml: str
    description: str
    python_method_name: str
    output_type: str
    output_yml: str


# Properties to receive via API on creation
class TaskDefinitionCreate(TaskDefinitionBase):
    pass


# Properties to receive via API on update
class TaskDefinitionUpdate(TaskDefinitionBase):
    pass


class TaskDefinitionInDBBase(TaskDefinitionBase):
    id: UUID
    created_date: datetime
    modified_date: datetime
    created_by_email: Optional[EmailStr] = None
    modified_by_email: Optional[EmailStr] = None
    deleted_at: Optional[datetime] = None  # New field to support soft deletes

    class Config:
        from_attributes = True


# Additional properties to return via API
class TaskDefinition(TaskDefinitionInDBBase):

    class Config:
        populate_by_name = True


# Additional properties stored in DB
class TaskDefinitionInDB(TaskDefinitionInDBBase):
    pass


class TaskDefinitionNamesList(BaseModel):
    task_definitions: list[str]


# TODO: Placeholder for data class to represent vectorized task definition in VDB
class TaskDefinitionInVectorDBBase(TaskDefinitionBase):
    pass
