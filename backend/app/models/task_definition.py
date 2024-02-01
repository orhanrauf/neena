from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import TYPE_CHECKING, Any, Dict
from uuid import uuid4
from app.core.shared_models import TaskParameter
from pydantic import BaseModel

from sqlalchemy import TEXT, DateTime, ForeignKey, String, TypeDecorator
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
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_name: Mapped[str] = mapped_column(String)
    integration: Mapped[str] = mapped_column(UUID, ForeignKey("integration.id"), nullable=False)
    parameters: Mapped[list[TaskParameter]] = mapped_column(TaskParameterType)
    python_method_name: Mapped[str] = mapped_column(String)
    python_code: Mapped[str] = mapped_column(String)
    output_type: Mapped[str] = mapped_column(String) # Should make pydantic type that has JSON and YML as serializable types
    description: Mapped[str] = mapped_column(String)
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=True)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    belongs_to_integration: Mapped["Integration"] = relationship("Integration", back_populates="task_definitions")

    created_by: Mapped["User"]  = relationship(back_populates="created_task_definitions", foreign_keys='TaskDefinition.created_by_email')
    modified_by: Mapped["User"]  = relationship(back_populates="modified_task_definitions", foreign_keys='TaskDefinition.modified_by_email')

    has_instances: Mapped[list["TaskOperation"]] = relationship(back_populates="is_instance_of", foreign_keys='TaskOperation.task_definition')
