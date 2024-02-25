from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Assuming FlowStatus is an enum or a valid Pydantic type, and TaskRunBase is defined elsewhere
from app.schemas.task_run import TaskRunBase 
from app.core.shared_models import FlowStatus  

# Shared properties
class FlowRunBase(BaseModel):
    flow: UUID
    status: FlowStatus
    triggered_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    triggered_by: Optional[str] = None

# Properties to receive via API on creation
class FlowRunCreate(FlowRunBase):
    pass

# Properties to receive via API on update
class FlowRunUpdate(FlowRunBase):
    pass

# Database model base
class FlowRunInDBBase(FlowRunBase):
    id: UUID
    task_runs: Optional[List[TaskRunBase]] = []

    class Config:
        from_attributes = True

# Additional properties to return via API
class FlowRun(FlowRunInDBBase):
    pass

# Additional properties stored in DB
class FlowRunInDB(FlowRunInDBBase):
    pass
