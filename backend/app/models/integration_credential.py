from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .integration import Integration
    from .user import User

class IntegrationCredential(Base):
    __tablename__ = 'integration_credential'
    __table_args__ = (
        UniqueConstraint('intergation', 'modified_by_email', name='uix_integration_modified_by'),
        UniqueConstraint('intergation', 'created_by_email', name='uix_integration_created_by')   
    )

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    intergation: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integration.id"), nullable=False)
    created_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    modified_by_email: Mapped[str] = mapped_column(String, ForeignKey("user.email"), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    # Relationship to User model for 'created_by' and 'modified_by'
    creator: Mapped["User"] = relationship("User", back_populates="created_credentials", foreign_keys=[created_by_email])
    modifier: Mapped["User"] = relationship("User", back_populates="modified_credentials", foreign_keys=[modified_by_email])
