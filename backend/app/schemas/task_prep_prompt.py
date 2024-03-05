from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class TaskPrepPromptBase(BaseModel):
    messages: list[dict[str, str]]

    class Config:
        from_attributes = True
        from_orm = True


# Properties to receive via API on creation
class TaskPrepPromptCreate(TaskPrepPromptBase):
    task_run: UUID


class TaskPrepPromptUpdate(TaskPrepPromptBase):
    pass


class TaskPrepPromptInDBBase(TaskPrepPromptBase):
    id: UUID
    created_date: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class TaskPrepPrompt(TaskPrepPromptInDBBase):
    pass


# Additional properties stored in DB
class TaskPrepPromptInDB(TaskPrepPromptInDBBase):
    pass
