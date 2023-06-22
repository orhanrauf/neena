from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.models.types.text_pickle import TextPickleType

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .task_operation import TaskOperation

class TaskParameter:
    name: str
    data_type: str
    position: int

class TaskDefinition(Base):
    
    __tablename__ = 'task_definition'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_name: Mapped[str] = mapped_column(String)
    parameters: Mapped[Optional[list]] = mapped_column(TextPickleType)
    output_type: Mapped[str] = mapped_column(String)
    output_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    python_code: Mapped[str] = mapped_column(String)
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False
    )

    created_by: Mapped["User"]  = relationship(back_populates="created_task_definitions", foreign_keys='TaskDefinition.created_by_email')
    modified_by: Mapped["User"]  = relationship(back_populates="modified_task_definitions", foreign_keys='TaskDefinition.modified_by_email')

    has_instances: Mapped[list["TaskOperation"]] = relationship(back_populates="is_instance_of", foreign_keys='TaskOperation.task_definition')