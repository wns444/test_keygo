from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Integer, DateTime, Enum, UniqueConstraint, Index
from app.models.base import Base


class TaskStatus(str, PyEnum):
    """Status enum for internal tasks."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class InternalTask(Base):
    """Internal Task model."""

    __tablename__ = "internal_tasks"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Ensure no duplicate tasks for the same booking with same title
    __table_args__ = (
        UniqueConstraint("booking_id", "title", name="uq_booking_title"),
        Index("idx_booking_status", "booking_id", "status"),
    )

    def __repr__(self):
        return f"<InternalTask(id={self.id}, booking_id={self.booking_id}, title={self.title}, status={self.status})>"
