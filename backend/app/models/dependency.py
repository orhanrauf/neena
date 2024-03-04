from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .task_operation import TaskOperation
    from .flow import Flow


class Dependency(Base):
    __tablename__ = "dependency"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    flow: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("flow.id"), nullable=False)
    source_task_operation: Mapped[Integer] = mapped_column(Integer, nullable=False)
    target_task_operation: Mapped[Integer] = mapped_column(Integer, nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    flow_reference: Mapped["Flow"] = relationship("Flow", back_populates="dependencies")

    source_task_operation_reference: Mapped["TaskOperation"] = relationship(
        "TaskOperation", foreign_keys=[source_task_operation]
    )
    target_task_operation_reference: Mapped["TaskOperation"] = relationship(
        "TaskOperation", foreign_keys=[target_task_operation]
    )

    __table_args__ = (
        UniqueConstraint("source_task_operation", "target_task_operation", "flow", name="_source_target_flow_uc"),
        ForeignKeyConstraint(["source_task_operation", "flow"], ["task_operation.index", "task_operation.flow"]),
        ForeignKeyConstraint(["target_task_operation", "flow"], ["task_operation.index", "task_operation.flow"]),
    )
