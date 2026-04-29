from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.internal_task import TaskStatus


class InternalTaskCreate(BaseModel):
    """Schema for creating an internal task."""
    booking_id: str = Field(..., min_length=1, max_length=50, description="Booking ID")
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

    @field_validator("booking_id", mode="before")
    @classmethod
    def validate_booking_id(cls, v):
        """Validate booking_id format."""
        if not v or not str(v).strip():
            raise ValueError("booking_id cannot be empty")
        return str(v).strip()

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v):
        """Validate title format."""
        if not v or not str(v).strip():
            raise ValueError("title cannot be empty")
        return str(v).strip()


class InternalTaskStatusUpdate(BaseModel):
    """Schema for updating task status."""
    status: TaskStatus = Field(..., description="New task status")


class InternalTaskUpdate(BaseModel):
    """Schema for updating an internal task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = Field(None)


class InternalTaskResponse(BaseModel):
    """Schema for returning an internal task."""
    id: int
    booking_id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
