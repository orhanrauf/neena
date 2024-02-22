from typing import Dict, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr

# Shared properties
class DependencyBase(BaseModel):
    instruction: Optional[constr(max_length=512)] = None

# Properties to receive via API on creation
class DependencyCreate(DependencyBase):
    flow: UUID
    source_task_operation: UUID
    target_task_operation: UUID

# Properties to receive via API on update
class DependencyUpdate(DependencyBase):
    flow: Optional[UUID] = None
    source_task_operation: Optional[UUID] = None
    target_task_operation: Optional[UUID] = None

class DependencyInDBBase(DependencyBase):
    id: Optional[UUID] = None
    flow: UUID
    source_task_operation: UUID
    target_task_operation: UUID

    class Config:
        from_attributes = True

# Additional properties to return via API
class Dependency(DependencyInDBBase):
    pass

# Additional properties stored in DB
class DependencyInDB(DependencyInDBBase):
    pass
