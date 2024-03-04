from typing import Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TaskPrepParameterBase(BaseModel):
    name: str
    value: Any
    explanation: Optional[str] = None


# Shared properties
class TaskPrepAnswerBase(BaseModel):
    parameters: list[TaskPrepParameterBase]

    class Config:
        from_attributes = True
        from_orm = True


# Properties to receive via API on creation
class TaskPrepAnswerCreate(TaskPrepAnswerBase):
    task_prep_prompt: UUID
    task_run: UUID


# Properties to receive via API on update
class TaskPrepAnswerUpdate(TaskPrepAnswerBase):
    pass


class TaskPrepAnswerInDBBase(TaskPrepAnswerBase):
    id: UUID
    created_date: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API


class TaskPrepAnswer(TaskPrepAnswerInDBBase):
    pass


# Additional properties stored in DB
class TaskPrepAnswerInDB(TaskPrepAnswerInDBBase):
    pass
