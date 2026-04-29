import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.internal_task import InternalTask, TaskStatus
from app.schemas.internal_task import (
    InternalTaskCreate,
    InternalTaskResponse,
    InternalTaskStatusUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["internal_tasks"])


@router.get("/bookings/{booking_id}/internal-tasks", response_model=list[InternalTaskResponse])
def get_internal_tasks(
    booking_id: str,
    status: TaskStatus | None = None,
    db: Session = Depends(get_db),
):
    """Get all internal tasks for a booking."""
    logger.info(f"Fetching internal tasks for booking {booking_id}")

    query = db.query(InternalTask).filter(InternalTask.booking_id == booking_id)

    if status:
        query = query.filter(InternalTask.status == status)

    tasks = query.all()
    logger.info(f"Found {len(tasks)} tasks for booking {booking_id}")
    return tasks


@router.post("/bookings/{booking_id}/internal-tasks", response_model=InternalTaskResponse, status_code=status.HTTP_201_CREATED)
def create_internal_task(
    booking_id: str,
    task_data: InternalTaskCreate,
    db: Session = Depends(get_db),
):
    """Create a new internal task for a booking."""
    logger.info(f"Creating internal task for booking {booking_id}: {task_data.title}")
    
    # Validate booking_id consistency
    if task_data.booking_id != booking_id:
        logger.warning(f"Booking ID mismatch: {task_data.booking_id} vs {booking_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="booking_id in path and body must match"
        )
    
    try:
        # Create new task
        db_task = InternalTask(
            booking_id=booking_id,
            title=task_data.title,
            description=task_data.description,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        logger.info(f"Successfully created internal task {db_task.id} for booking {booking_id}")
        return db_task
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Duplicate task error for booking {booking_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task with title '{task_data.title}' already exists for this booking"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating internal task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create internal task"
        )


@router.get("/internal-tasks/{task_id}", response_model=InternalTaskResponse)
def get_internal_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific internal task."""
    logger.info(f"Fetching internal task {task_id}")
    
    task = db.query(InternalTask).filter(InternalTask.id == task_id).first()
    
    if not task:
        logger.warning(f"Internal task {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internal task not found"
        )
    
    return task


@router.patch("/internal-tasks/{task_id}/status", response_model=InternalTaskResponse)
def update_task_status(
    task_id: int,
    status_update: InternalTaskStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update the status of an internal task."""
    logger.info(f"Updating status of internal task {task_id} to {status_update.status}")
    
    task = db.query(InternalTask).filter(InternalTask.id == task_id).first()
    
    if not task:
        logger.warning(f"Internal task {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internal task not found"
        )
    
    try:
        task.status = status_update.status
        db.commit()
        db.refresh(task)
        
        logger.info(f"Successfully updated status of internal task {task_id} to {status_update.status}")
        return task
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task status"
        )


@router.delete("/internal-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_internal_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Delete an internal task."""
    logger.info(f"Deleting internal task {task_id}")
    
    task = db.query(InternalTask).filter(InternalTask.id == task_id).first()
    
    if not task:
        logger.warning(f"Internal task {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internal task not found"
        )
    
    try:
        db.delete(task)
        db.commit()
        logger.info(f"Successfully deleted internal task {task_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete internal task"
        )
