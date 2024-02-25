from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class TaskPrepPromptBase(BaseModel):
    body: str

# Properties to receive via API on creation
class TaskPrepPromptCreate(TaskPrepPromptBase):
    task_run_id: UUID

# Properties to receive via API on update
class TaskPrepPromptUpdate(TaskPrepPromptBase):
    task_run_id: Optional[UUID] = None
    body: Optional[str] = None

class TaskPrepPromptInDBBase(TaskPrepPromptBase):
    id: Optional[UUID] = None
    created_date: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class TaskPrepPrompt(TaskPrepPromptInDBBase):
    pass

# Additional properties stored in DB
class TaskPrepPromptInDB(TaskPrepPromptInDBBase):
    pass
