from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import TYPE_CHECKING, Any, Dict
from uuid import uuid4
import uuid
from app.core.shared_models import TaskParameter
from pydantic import BaseModel

from sqlalchemy import TEXT, Column, DateTime, ForeignKey, String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .task_operation import TaskOperation
    from .integration import Integration


class TaskParameterType(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            if all(isinstance(param, dict) for param in value):
                return json.dumps(value)
            else:
                return json.dumps([param.dict() for param in value])
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return [TaskParameter.from_dict(data) for data in json.loads(value)]
        return None

class TaskDefinition(Base):
    __tablename__ = 'task_definition'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)  # Ensure uuid is imported
    task_name = Column(String(64), nullable=False)  # Adjusted length according to Pydantic model constraints
    integration = Column(UUID(as_uuid=True), ForeignKey("integration.id"), nullable=False)  # Ensure it points to the integration table
    parameters: Mapped[list[TaskParameter]] = mapped_column(TaskParameterType)
    python_method_name = Column(String, nullable=False)
    input_type = Column(String, nullable=False)
    input_yml = Column(String, nullable=False)  
    output_type = Column(String, nullable=False)
    output_yml = Column(String, nullable=False)  
    description = Column(String, nullable=False)
    
    created_by_email = Column(String, ForeignKey("user.email"))  # Nullable by default, matches Pydantic
    modified_by_email = Column(String, ForeignKey("user.email"))  # Nullable by default, matches Pydantic
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # For soft deletes

    # Adjust relationship definitions as needed based on your models
    belongs_to_integration = relationship("Integration", back_populates="task_definitions")
    created_by = relationship("User", foreign_keys=[created_by_email], back_populates="created_task_definitions")
    modified_by = relationship("User", foreign_keys=[modified_by_email], back_populates="modified_task_definitions")

    has_instances: Mapped[list["TaskOperation"]] = relationship(back_populates="is_instance_of", foreign_keys='TaskOperation.task_definition')
