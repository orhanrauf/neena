from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class TaskPrepAnswerBase(BaseModel):
    natural_language_explanation: str
    body: str
    has_python_execution: bool

# Properties to receive via API on creation
class TaskPrepAnswerCreate(TaskPrepAnswerBase):
    task_prep_prompt_id: UUID
    task_run_id: UUID

# Properties to receive via API on update
class TaskPrepAnswerUpdate(TaskPrepAnswerBase):
    task_prep_prompt_id: Optional[UUID] = None
    task_run_id: Optional[UUID] = None
    natural_language_explanation: Optional[str] = None
    body: Optional[str] = None
    has_python_execution: Optional[bool] = None

class TaskPrepAnswerInDBBase(TaskPrepAnswerBase):
    id: Optional[UUID] = None
    created_date: datetime

    class Config:
        orm_mode = True

# Additional properties to return via API

class TaskPrepAnswer(TaskPrepAnswerInDBBase):
    pass

# Additional properties stored in DB
class TaskPrepAnswerInDB(TaskPrepAnswerInDBBase):
    pass
