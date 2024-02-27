from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.shared_models import TaskStatus

from pydantic import BaseModel

from app.schemas.task_prep_prompt import TaskPrepPromptBase
from app.schemas.task_prep_answer import TaskPrepAnswerBase


class TaskRunBase(BaseModel):
    task_operation_id: UUID
    flow_run_id: UUID
    status: TaskStatus
    task_prep_prompt: Optional[TaskPrepPromptBase] = None
    task_prep_answer: Optional[TaskPrepAnswerBase] = None
    start_time: datetime
    result: dict
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True


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
