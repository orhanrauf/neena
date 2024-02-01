from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.shared_models import TaskStatus

from pydantic import BaseModel

class TaskRunBase(BaseModel):
    task_operation_id: UUID
    flow_run_id: UUID
    status: TaskStatus
    start_time: datetime
    result: dict
    end_time: Optional[datetime] = None

    class Config:
        orm_mode = True

class TaskRunCreate(TaskRunBase):
    pass


class TaskRunUpdate(TaskRunBase):
    pass


class TaskRunInDBBase(TaskRunBase):
    id: UUID
    
    
    class Config:
        orm_mode = True

class TaskRun(TaskRunInDBBase):
    pass