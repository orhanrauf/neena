from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, create_engine, Text, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import datetime

class TaskLog(Base):
    __tablename__ = "task_log"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    timestamp_utc = Column(DateTime, default=datetime.datetime.utcnow, index=True)  # Automatically set to the current time
    message = Column(Text)
    task_run_id = Column(UUID(as_uuid=True), ForeignKey("task_run.id"), index=True)
    flow_run_id = Column(UUID(as_uuid=True), ForeignKey("flow_run.id"))
    task_run = relationship("TaskRun", back_populates="logs")
    flow_run = relationship("FlowRun", back_populates="logs")