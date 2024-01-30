from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import json
from typing import TYPE_CHECKING, Any, Dict, Optional

from uuid import uuid4
from app.core.shared_models import Argument
from attr import asdict
from pydantic import BaseModel

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from sqlalchemy.types import TypeDecorator, Text

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .flow import Flow
    from .task_definition import TaskDefinition
    from .task_run import TaskRun

class TaskOperation(Base):
    
    __tablename__ = 'task_operation'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    flow: Mapped[UUID] = mapped_column(UUID, ForeignKey("flow.id"), nullable=False)
    task_definition: Mapped[UUID] = mapped_column(UUID, ForeignKey("task_definition.id"), nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String)
    
    
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    
    
    organization: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
    
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    
    belongs_to_flow: Mapped["Flow"]  = relationship(back_populates="task_operations", foreign_keys='TaskOperation.flow')
    is_instance_of: Mapped["TaskDefinition"]  = relationship(back_populates="has_instances", foreign_keys='TaskOperation.task_definition')

    created_by: Mapped["User"] = relationship(back_populates="created_task_operations", foreign_keys='TaskOperation.created_by_email')
    modified_by: Mapped["User"]  = relationship(back_populates="modified_task_operations", foreign_keys='TaskOperation.modified_by_email')
    task_runs: Mapped[list["TaskRun"]] = relationship("TaskRun", back_populates="is_instance_of_task_operation")
