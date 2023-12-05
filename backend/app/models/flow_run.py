from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class FlowRun(Base):
    __tablename__ = "flow_run"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("flow.id"), nullable=False)
    status = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True))
    task_runs = relationship("TaskRun", back_populates="flow_run", cascade="all, delete-orphan")
    logs = relationship("TaskLog", back_populates="flow_run")
    flow = relationship("Flow", back_populates="flow_runs")