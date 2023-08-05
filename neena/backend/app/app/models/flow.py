from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .flow_request import FlowRequest
    from .task_operation import TaskOperation
    

class Flow(Base):
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    flow_request: Mapped[UUID] = mapped_column(UUID, ForeignKey("flow_request.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, index=True, default=uuid4, nullable=True)
    
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
    
    created_by_human: Mapped[bool] = mapped_column(Boolean)
    modified_by_human: Mapped[bool] = mapped_column(Boolean)

    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    
    task_operations: Mapped[list["TaskOperation"]] = relationship(back_populates="belongs_to_flow", foreign_keys='TaskOperation.flow', cascade="all, delete-orphan")
    created_for: Mapped["FlowRequest"] = relationship(back_populates="flow", uselist=False, foreign_keys='Flow.flow_request')
    created_by: Mapped["User"]  = relationship(back_populates="created_flows", foreign_keys='Flow.created_by_email')
    modified_by: Mapped["User"]  = relationship(back_populates="modified_flows", foreign_keys='Flow.modified_by_email')
    