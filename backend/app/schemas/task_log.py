from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TaskLogBase(BaseModel):
    timestamp_utc: datetime
    message: str

class TaskLogCreate(TaskLogBase):
    task_run_id: UUID
    flow_run_id: UUID

class TaskLog(TaskLogBase):
    id: UUID
    task_run_id: UUID
    flow_run_id: UUID

    class Config:
        from_attributes = True
