
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base_class import Base


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    auth0_id = Column(String, unique=True, index=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    