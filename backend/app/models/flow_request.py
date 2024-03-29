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
    from .flow import Flow


class FlowRequest(Base):
    
    __tablename__ = 'flow_request'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    
    request_name: Mapped[str] = mapped_column(String, nullable=True)
    request_instructions: Mapped[str] = mapped_column(String, nullable=False)  
    request_metadata: Mapped[Optional[list[dict]]] = mapped_column(TextPickleType, nullable=True)
    flow: Mapped[UUID] = mapped_column(UUID, ForeignKey("flow.id"), nullable=True)
    
    organization: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    
    created_by: Mapped["User"]  = relationship(back_populates="created_flow_requests", foreign_keys='FlowRequest.created_by_email')
    modified_by: Mapped["User"]  = relationship(back_populates="modified_flow_requests", foreign_keys='FlowRequest.modified_by_email')
    
    belongs_to_flow: Mapped["Flow"] = relationship("Flow", back_populates="flow_requests")