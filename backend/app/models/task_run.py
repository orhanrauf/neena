from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class TaskRun(Base):
    __tablename__ = "task_run"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_operation_id = Column(UUID(as_uuid=True), ForeignKey("task_operation.id"), nullable=False)
    flow_run_id = Column(UUID(as_uuid=True), ForeignKey("flow_run.id"), nullable=False)
    status = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True))
    logs = relationship("TaskLog", back_populates="task_run", cascade="all, delete-orphan")
    task_operation = relationship("TaskOperation", back_populates="task_runs")
    flow_run = relationship("FlowRun", back_populates="task_runs")
    