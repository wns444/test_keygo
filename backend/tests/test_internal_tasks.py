import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestInternalTaskAPI:
    """Test suite for Internal Task API."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    # Task Creation Tests
    def test_create_internal_task_success(self):
        """Test successful creation of internal task."""
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue with payment",
            "description": "Customer reported charge issue"
        }

        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["booking_id"] == "BOOKING123"
        assert data["title"] == "Issue with payment"
        assert data["description"] == "Customer reported charge issue"
        assert data["status"] == "open"
        assert data["id"] is not None

    def test_create_task_without_description(self):
        """Test creating task without optional description."""
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue with payment"
        }

        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["description"] is None

    def test_create_task_invalid_booking_id_in_path(self):
        """Test booking_id mismatch between path and body."""
        task_data = {
            "booking_id": "BOOKING456",
            "title": "Issue with payment"
        }

        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )

        assert response.status_code == 400
        assert "match" in response.json()["detail"].lower()

    def test_create_task_empty_title(self):
        """Test creating task with empty title."""
        task_data = {
            "booking_id": "BOOKING123",
            "title": ""
        }
        
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_task_missing_title(self):
        """Test creating task without required title."""
        task_data = {
            "booking_id": "BOOKING123"
        }
        
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        
        assert response.status_code == 422
    
    def test_create_task_empty_booking_id(self):
        """Test creating task with empty booking_id."""
        task_data = {
            "booking_id": "",
            "title": "Issue"
        }
        
        response = client.post(
            "/api/v1/bookings/EMPTY/internal-tasks",
            json=task_data
        )
        
        # Will be 422 for empty booking_id in body validation
        assert response.status_code == 422
    
    # Duplicate Prevention Tests
    def test_prevent_duplicate_task(self):
        """Test that duplicate tasks for same booking are prevented."""
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Payment issue"
        }
        
        # Create first task
        response1 = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"]
    
    def test_allow_same_title_different_booking(self):
        """Test that same title is allowed for different bookings."""
        task_data1 = {
            "booking_id": "BOOKING123",
            "title": "Payment issue"
        }
        
        task_data2 = {
            "booking_id": "BOOKING456",
            "title": "Payment issue"
        }
        
        response1 = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data1
        )
        assert response1.status_code == 201
        
        response2 = client.post(
            "/api/v1/bookings/BOOKING456/internal-tasks",
            json=task_data2
        )
        assert response2.status_code == 201
    
    # Task Retrieval Tests
    def test_get_all_tasks_for_booking(self):
        """Test retrieving all tasks for a booking."""
        # Create multiple tasks
        for i in range(3):
            task_data = {
                "booking_id": "BOOKING123",
                "title": f"Issue {i}"
            }
            client.post(
                "/api/v1/bookings/BOOKING123/internal-tasks",
                json=task_data
            )
        
        response = client.get("/api/v1/bookings/BOOKING123/internal-tasks")
        
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3
    
    def test_get_tasks_by_status(self):
        """Test retrieving tasks filtered by status."""
        # Create tasks
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue 1"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        # Get open tasks
        response = client.get(
            "/api/v1/bookings/BOOKING123/internal-tasks?status=open"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        
        # Change status to resolved
        client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "resolved"}
        )
        
        # Get open tasks (should be empty)
        response = client.get(
            "/api/v1/bookings/BOOKING123/internal-tasks?status=open"
        )
        assert len(response.json()) == 0
        
        # Get resolved tasks
        response = client.get(
            "/api/v1/bookings/BOOKING123/internal-tasks?status=resolved"
        )
        assert len(response.json()) == 1
    
    def test_get_tasks_empty_booking(self):
        """Test retrieving tasks for booking with no tasks."""
        response = client.get("/api/v1/bookings/NONEXISTENT/internal-tasks")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_specific_task(self):
        """Test retrieving a specific task by ID."""
        # Create task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Payment issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        # Get specific task
        response = client.get(f"/api/v1/internal-tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Payment issue"
    
    def test_get_nonexistent_task(self):
        """Test retrieving non-existent task."""
        response = client.get("/api/v1/internal-tasks/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    # Status Update Tests
    def test_update_task_status(self):
        """Test updating task status."""
        # Create task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Payment issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        # Update status
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "in_progress"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"
    
    def test_update_status_to_resolved(self):
        """Test updating status to resolved."""
        # Create and update task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "resolved"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"
    
    def test_update_status_to_closed(self):
        """Test updating status to closed."""
        # Create and update task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "closed"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "closed"
    
    def test_update_status_invalid_task(self):
        """Test updating status for non-existent task."""
        response = client.patch(
            "/api/v1/internal-tasks/99999/status",
            json={"status": "resolved"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_update_status_invalid_value(self):
        """Test updating status with invalid value."""
        # Create task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        # Try to update with invalid status
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "invalid_status"}
        )
        
        assert response.status_code == 422
    
    # Delete Tests
    def test_delete_internal_task(self):
        """Test deleting an internal task."""
        # Create task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Issue"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        task_id = response.json()["id"]
        
        # Delete task
        response = client.delete(f"/api/v1/internal-tasks/{task_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/api/v1/internal-tasks/{task_id}")
        assert response.status_code == 404
    
    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task."""
        response = client.delete("/api/v1/internal-tasks/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    # Integration Tests
    def test_complete_workflow(self):
        """Test complete workflow: create, retrieve, update status, delete."""
        # 1. Create task
        task_data = {
            "booking_id": "BOOKING123",
            "title": "Payment issue",
            "description": "Customer reports failed charge"
        }
        response = client.post(
            "/api/v1/bookings/BOOKING123/internal-tasks",
            json=task_data
        )
        assert response.status_code == 201
        task_id = response.json()["id"]
        
        # 2. Retrieve task
        response = client.get(f"/api/v1/internal-tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "open"
        
        # 3. Update status to in_progress
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "in_progress"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
        
        # 4. Update status to resolved
        response = client.patch(
            f"/api/v1/internal-tasks/{task_id}/status",
            json={"status": "resolved"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"
        
        # 5. Delete task
        response = client.delete(f"/api/v1/internal-tasks/{task_id}")
        assert response.status_code == 204
    
    def test_multiple_bookings_isolation(self):
        """Test that tasks are properly isolated by booking."""
        # Create tasks for different bookings
        booking1_task = {
            "booking_id": "BOOKING1",
            "title": "Issue 1"
        }
        booking2_task = {
            "booking_id": "BOOKING2",
            "title": "Issue 2"
        }
        
        client.post(
            "/api/v1/bookings/BOOKING1/internal-tasks",
            json=booking1_task
        )
        client.post(
            "/api/v1/bookings/BOOKING2/internal-tasks",
            json=booking2_task
        )
        
        # Get tasks for booking 1
        response = client.get("/api/v1/bookings/BOOKING1/internal-tasks")
        assert len(response.json()) == 1
        assert response.json()[0]["booking_id"] == "BOOKING1"
        
        # Get tasks for booking 2
        response = client.get("/api/v1/bookings/BOOKING2/internal-tasks")
        assert len(response.json()) == 1
        assert response.json()[0]["booking_id"] == "BOOKING2"
