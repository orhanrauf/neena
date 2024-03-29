from typing import Dict, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr


# Shared properties
class DependencyBase(BaseModel):
    instruction: Optional[constr(max_length=512)] = None
    source_task_operation: int
    target_task_operation: int


class DependencyList(BaseModel):
    dependencies: list[DependencyBase]


# Properties to receive via API on creation
class DependencyCreate(DependencyBase):
    flow: UUID


# Properties to receive via API on update
class DependencyUpdate(DependencyBase):
    id: Optional[UUID] = None
    flow: Optional[UUID] = None


class DependencyInDBBase(DependencyBase):
    id: UUID
    flow: UUID

    class Config:
        from_attributes = True
        from_orm = True


# Additional properties to return via API
class Dependency(DependencyInDBBase):
    pass


# Additional properties stored in DB
class DependencyInDB(DependencyInDBBase):
    pass
