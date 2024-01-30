from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .task_run import TaskRun
    from .task_prep_answer import TaskPrepAnswer

class TaskPrepPrompt(Base):
    __tablename__ = 'task_prep_prompt'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_run: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task_run.id"), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Assuming TaskRun is another model that relates to TaskPrepPrompt
    belongs_to_task_run: Mapped["TaskRun"] = relationship("TaskRun", back_populates="task_prep_prompts")
    has_answer: Mapped[list["TaskPrepAnswer"]] = relationship("TaskPrepAnswer", back_populates="belongs_to_task_prep_prompt")
