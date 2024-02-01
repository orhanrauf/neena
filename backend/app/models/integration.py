from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base

class Integration(Base):
    __tablename__ = 'integration'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    uses_api_key = Column(Boolean, default=False, nullable=False)
    uses_sso_key = Column(Boolean, default=False, nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    task_definitions = relationship('TaskDefinition', back_populates='belongs_to_integration')
    