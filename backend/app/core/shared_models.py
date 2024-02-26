from enum import Enum
from typing import Any, Dict, Type, TYPE_CHECKING
from pydantic import BaseModel

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    
class FlowStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"    

class TaskParameter(BaseModel):
    name: str
    data_type: str
    position: int
    doc_string: str
    optional: bool

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TaskParameter":
        return TaskParameter(**data)
    
class Argument(BaseModel):
    name: str
    data_type: str
    value: str
    source: str
    
    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Argument":
        return Argument(**data)
    
    class Config:
        from_attributes = True
