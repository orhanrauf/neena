from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import ARRAY, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from . import IntegrationCredential  # noqa: F401
    from . import FlowRequest # noqa: F401
    from . import TaskDefinition
    from . import Flow
    from . import TaskOperation
    from . import FlowRun

class User(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    auth0_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    organization: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)

    permissions: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    full_name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime( timezone=True), server_default=func.now(), nullable=False)
    
    created_flow_requests: Mapped[list["FlowRequest"]] = relationship(back_populates="created_by", lazy="dynamic", foreign_keys='FlowRequest.created_by_email')
    modified_flow_requests: Mapped[list["FlowRequest"]] = relationship(back_populates="modified_by", lazy="dynamic", foreign_keys='FlowRequest.modified_by_email')
    created_task_definitions: Mapped[list["TaskDefinition"]] = relationship(back_populates="created_by", lazy="dynamic", foreign_keys='TaskDefinition.created_by_email')
    modified_task_definitions: Mapped[list["TaskDefinition"]] = relationship(back_populates="modified_by", lazy="dynamic", foreign_keys='TaskDefinition.modified_by_email')
    created_flows: Mapped[list["Flow"]] = relationship(back_populates="created_by", lazy="dynamic", foreign_keys='Flow.created_by_email')
    modified_flows: Mapped[list["Flow"]] = relationship(back_populates="modified_by", lazy="dynamic", foreign_keys='Flow.modified_by_email')
    created_task_operations: Mapped[list["TaskOperation"]] = relationship(back_populates="created_by", lazy="dynamic", foreign_keys='TaskOperation.created_by_email')
    modified_task_operations: Mapped[list["TaskOperation"]] = relationship(back_populates="modified_by", lazy="dynamic", foreign_keys='TaskOperation.modified_by_email')
    
    created_flow_runs: Mapped[list["FlowRun"]] = relationship(back_populates="created_by", foreign_keys='FlowRun.created_by_email')
    modified_flow_runs: Mapped[list["FlowRun"]] = relationship(back_populates="modified_by", foreign_keys='FlowRun.modified_by_email')
    
    created_credentials: Mapped[list["IntegrationCredential"]] = relationship("IntegrationCredential", back_populates="creator", foreign_keys='IntegrationCredential.created_by_email')
    modified_credentials: Mapped[list["IntegrationCredential"]] = relationship("IntegrationCredential", back_populates="modifier", foreign_keys='IntegrationCredential.modified_by_email')