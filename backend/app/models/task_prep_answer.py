from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, JSON, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint

from app.db.base_class import Base

if TYPE_CHECKING:
    from .task_run import TaskRun
    from .task_prep_prompt import TaskPrepPrompt


class TaskPrepAnswer(Base):
    __tablename__ = "task_prep_answer"

    # Unique constraints
    __table_args__ = (
        UniqueConstraint("task_prep_prompt", name="uix_task_prep_prompt"),
        UniqueConstraint("task_run", name="uix_task_run_and_answer"),
    )

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_prep_prompt: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("task_prep_prompt.id"), nullable=False
    )
    task_run: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task_run.id"), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=True)
    parameters: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=False)

    created_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    belongs_to_task_prep_prompt: Mapped["TaskPrepPrompt"] = relationship("TaskPrepPrompt", back_populates="has_answer")
    belongs_to_task_run: Mapped["TaskRun"] = relationship("TaskRun", back_populates="task_prep_answer")
