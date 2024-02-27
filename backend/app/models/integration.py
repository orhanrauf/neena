from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base

class Integration(Base):
    __tablename__ = 'integration'
    __table_args__ = (
        UniqueConstraint('short_name', name='short_name_unique_constraint'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    class_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    uses_api_key = Column(Boolean, default=False, nullable=True)
    uses_sso_key = Column(Boolean, default=False, nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    task_definitions = relationship('TaskDefinition', back_populates='belongs_to_integration')
    credentials = relationship('IntegrationCredential', back_populates='credential_of')
    