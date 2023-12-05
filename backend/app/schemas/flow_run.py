from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.shared_models import FlowStatus
from .task_run import TaskRunBase

from pydantic import BaseModel

class FlowRunBase(BaseModel):
    flow_id: UUID
    status: FlowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    task_runs: Optional[List[TaskRunBase]]

    class Config:
        orm_mode = True


class FlowRunCreate(FlowRunBase):
    pass


class FlowRunUpdate(FlowRunBase):
    pass


class FlowRunInDBBase(FlowRunBase):
    id: UUID

    class Config:
        orm_mode = True

class FlowRun(FlowRunInDBBase):
    pass