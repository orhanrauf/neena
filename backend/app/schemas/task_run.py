from typing import Any, Optional
from uuid import UUID
from datetime import datetime
from app.core.shared_models import TaskStatus

from pydantic import BaseModel

from app.schemas.task_prep_prompt import TaskPrepPromptBase
from app.schemas.task_prep_answer import TaskPrepAnswerBase


class TaskRunBase(BaseModel):
    flow_run: UUID
    task_operation_index: int
    status: TaskStatus
    start_time: datetime
    task_prep_prompt: Optional[TaskPrepPromptBase] = None
    task_prep_answer: Optional[TaskPrepAnswerBase] = None
    result: Optional[dict | list] = None  # TODO: encapsulate this in a Result class
    end_time: Optional[datetime] = None

    class Config:
        from_orm = True


class TaskRunCreate(TaskRunBase):
    pass


class TaskRunUpdate(TaskRunBase):
    pass


class TaskRunInDBBase(TaskRunBase):
    id: UUID

    class Config:
        from_attributes = True


class TaskRun(TaskRunInDBBase):
    pass
