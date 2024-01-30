import json
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import TEXT, Column, JSON, String, DateTime, ForeignKey, Enum as SqlAlchemyEnum, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.core.shared_models import Argument, TaskStatus


if TYPE_CHECKING:
    from .task_prep_prompt import TaskPrepPrompt
    from .task_prep_answer import TaskPrepAnswer
    from .task_operation import TaskOperation
    
class ArgumentType(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            if all(isinstance(param, dict) for param in value):
                return json.dumps(value)
            else:
                return json.dumps([param.to_dict() for param in value])
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return [Argument.from_dict(data) for data in json.loads(value)]
        return None

class TaskRun(Base):
    __tablename__ = "task_run"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_operation = Column(UUID(as_uuid=True), ForeignKey
                               ("task_operation.id"), nullable=False)
    flow_run = Column(UUID(as_uuid=True), ForeignKey
                               ("flow_run.id"))
    status = Column(SqlAlchemyEnum(TaskStatus), nullable=False) 
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True))
    result = Column(JSON, nullable=True)
    
    arguments: Mapped[list[Argument]] = mapped_column(ArgumentType)
    
    belongs_to_flow_run = relationship("FlowRun", back_populates="task_runs")
    is_instance_of_task_operation = relationship("TaskOperation", back_populates="task_runs")
    

    
    task_prep_prompts: Mapped[list["TaskPrepPrompt"]] = relationship("TaskPrepPrompt", back_populates="belongs_to_task_run")
    task_prep_answers: Mapped[list["TaskPrepAnswer"]] = relationship("TaskPrepAnswer", back_populates="belongs_to_task_run")
    
    