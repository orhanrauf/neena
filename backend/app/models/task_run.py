from datetime import datetime
import json
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import TEXT, Column, Integer, JSON, String, DateTime, ForeignKey, Enum as SqlAlchemyEnum, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.core.shared_models import TaskStatus


if TYPE_CHECKING:
    from .task_prep_prompt import TaskPrepPrompt
    from .task_prep_answer import TaskPrepAnswer


class TaskRun(Base):
    __tablename__ = "task_run"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    flow_run = Column(UUID(as_uuid=True), ForeignKey("flow_run.id"))
    task_operation_index = Column(Integer, nullable=False)
    status = Column(SqlAlchemyEnum(TaskStatus), nullable=False)
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True))
    result = Column(JSON, nullable=True)

    belongs_to_flow_run = relationship("FlowRun", back_populates="task_runs")
    
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    task_prep_prompt: Mapped["TaskPrepPrompt"] = relationship("TaskPrepPrompt", back_populates="belongs_to_task_run")
    task_prep_answer: Mapped["TaskPrepAnswer"] = relationship("TaskPrepAnswer", back_populates="belongs_to_task_run")
    
    