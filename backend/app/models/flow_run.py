from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SqlAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy.sql import func
from app.db.base_class import Base
from app.core.shared_models import FlowStatus


class FlowRun(Base):
    __tablename__ = "flow_run"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    organization: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)
    flow = Column(UUID(as_uuid=True), ForeignKey("flow.id"), nullable=False)
    status = Column(SqlAlchemyEnum(FlowStatus), nullable=False)
    triggered_time = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    triggered_by = Column(String, ForeignKey("user.email"), nullable=True)
    
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    task_runs = relationship("TaskRun", back_populates="belongs_to_flow_run", cascade="all, delete-orphan")
    belongs_to_flow = relationship("Flow", back_populates="flow_runs")
    
    created_by = relationship("User", back_populates="created_flow_runs")
    modified_by = relationship("User", back_populates="modified_flow_runs")
