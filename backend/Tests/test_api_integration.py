import pytest
import os

# Set testing environment BEFORE any other imports
os.environ["TESTING"] = "true"
print(f"🔍 TESTING environment variable set to: {os.environ.get('TESTING')}")

from fastapi.testclient import TestClient
from main import app
from db.database import Base, engine
from sqlalchemy.orm import sessionmaker
from services.auth_service import create_user, create_access_token

# Create a test database session
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def auth_headers():
    """Create a test user and return authentication headers"""
    from db.database import get_db
    from models.user import User
    db = next(get_db())
    
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        
        if not test_user:
            # Create test user if it doesn't exist
            test_user = create_user(
                email="test@example.com",
                password="testpassword",
                full_name="Test User",
                db=db
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": str(test_user.id)})
        
        return {"Authorization": f"Bearer {access_token}"}
    finally:
        db.close()

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Close all connections to prevent hanging
    engine.dispose()

# Debug test to check if auth_headers fixture works
def test_auth_headers_fixture(auth_headers):
    print("Auth headers:", auth_headers)
    assert "Authorization" in auth_headers
    assert auth_headers["Authorization"].startswith("Bearer ")
    print("✅ Auth headers fixture works!")

### Caregiver Tests ###
def test_add_caregiver_success(setup_database, auth_headers):
    with TestClient(app) as client:
        response = client.post("/caregivers/", json={
            "custom_id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

def test_add_existing_caregiver(setup_database, auth_headers):
    with TestClient(app) as client:
        client.post("/caregivers/", json={
            "custom_id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        response = client.post("/caregivers/", json={
            "custom_id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Caregiver with this ID already exists for this user"

def test_get_caregivers_success(setup_database, auth_headers):
    with TestClient(app) as client:
        client.post("/caregivers/", json={
            "custom_id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        response = client.get("/caregivers/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

def test_delete_nonexistent_caregiver(setup_database, auth_headers):
    with TestClient(app) as client:
        response = client.delete("/caregivers/99", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Caregiver not found"

### Elderly Tests ###
def test_add_elderly_success(setup_database, auth_headers):
    with TestClient(app) as client:
        response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Alice"

def test_add_existing_elderly(setup_database, auth_headers):
    with TestClient(app) as client:
        client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Elderly with this ID already exists for this user"

def test_get_elderly_success(setup_database, auth_headers):
    with TestClient(app) as client:
        client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        response = client.get("/elderly/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

def test_add_task_to_elderly_success(setup_database, auth_headers):
    with TestClient(app) as client:
        # Create elderly first
        elderly_response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        # Add task using the internal ID
        response = client.post(f"/elderly/{elderly_id}/tasks", json={
            "description": "Take medicine",
            "status": "pending"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["description"] == "Take medicine"

def test_add_task_to_nonexistent_elderly(setup_database, auth_headers):
    with TestClient(app) as client:
        response = client.post("/elderly/99/tasks", json={
            "description": "Take medicine",
            "status": "pending"
        }, headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Elderly not found"

### Medication Tests ###

def test_add_medication_to_elderly_success(setup_database, auth_headers):
    # Add an elderly person first
    with TestClient(app) as client:
        elderly_response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        # Add a medication for the elderly person
        response = client.post(f"/elderly/{elderly_id}/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Aspirin"

def test_add_medication_to_nonexistent_elderly(setup_database, auth_headers):
    with TestClient(app) as client:
        # Attempt to add medication for a non-existent elderly person
        response = client.post("/elderly/99/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        }, headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Elderly not found"

def test_get_medications_for_elderly_success(setup_database, auth_headers):
    # Add an elderly person and medications
    with TestClient(app) as client:
        elderly_response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        client.post(f"/elderly/{elderly_id}/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        }, headers=auth_headers)
        client.post(f"/elderly/{elderly_id}/medications", json={
            "name": "Ibuprofen",
            "dosage": "200mg",
            "frequency": "Twice a day"
        }, headers=auth_headers)
        
        # Retrieve medications for the elderly person
        response = client.get(f"/elderly/{elderly_id}/medications", headers=auth_headers)
        assert response.status_code == 200
        medications = response.json()
        assert len(medications) == 2
        assert medications[0]["name"] == "Aspirin"
        assert medications[1]["name"] == "Ibuprofen"

def test_delete_medication_from_elderly_success(setup_database, auth_headers):
    # Add an elderly person and a medication
    with TestClient(app) as client:
        elderly_response = client.post("/elderly/", json={
            "custom_id": 1,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        medication_response = client.post(f"/elderly/{elderly_id}/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        }, headers=auth_headers)
        medication_id = medication_response.json()["id"]  # Get the medication ID
        
        # Delete the medication
        response = client.delete(f"/elderly/{elderly_id}/medications/{medication_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Medication 'Aspirin' deleted successfully"

def test_delete_nonexistent_medication_from_elderly(setup_database, auth_headers):
    with TestClient(app) as client:
        # Attempt to delete a non-existent medication
        response = client.delete("/elderly/1/medications/99", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Medication not found"

### Caregiver Assignment Tests ###
def test_create_assignment_success(setup_database, auth_headers):
    # Add caregiver and elderly
    with TestClient(app) as client:
        caregiver_response = client.post("/caregivers/", json={
            "custom_id": 101,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        caregiver_id = caregiver_response.json()["id"]  # Get the internal ID
        
        elderly_response = client.post("/elderly/", json={
            "custom_id": 201,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID

        # Create assignment
        response = client.post("/caregiver-assignments/", json={
            "caregiver_id": caregiver_id,
            "elderly_id": elderly_id
        }, headers=auth_headers)
        assert response.status_code == 200
        assignment = response.json()
        assert assignment["caregiver_id"] == caregiver_id
        assert assignment["elderly_id"] == elderly_id

def test_create_assignment_with_nonexistent_caregiver(setup_database, auth_headers):
    # Add elderly
    with TestClient(app) as client:
        elderly_response = client.post("/elderly/", json={
            "custom_id": 201,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID

        # Attempt to create assignment with non-existent caregiver
        response = client.post("/caregiver-assignments/", json={
            "caregiver_id": 999,  # Non-existent caregiver
            "elderly_id": elderly_id
        }, headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Caregiver not found"

def test_create_assignment_with_nonexistent_elderly(setup_database, auth_headers):
    # Add caregiver
    with TestClient(app) as client:
        caregiver_response = client.post("/caregivers/", json={
            "custom_id": 101,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        caregiver_id = caregiver_response.json()["id"]  # Get the internal ID

        # Attempt to create assignment with non-existent elderly
        response = client.post("/caregiver-assignments/", json={
            "caregiver_id": caregiver_id,
            "elderly_id": 999  # Non-existent elderly
        }, headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Elderly not found"

def test_delete_assignment_success(setup_database, auth_headers):
    # Add caregiver, elderly, and assignment
    with TestClient(app) as client:
        caregiver_response = client.post("/caregivers/", json={
            "custom_id": 101,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        caregiver_id = caregiver_response.json()["id"]  # Get the internal ID
        
        elderly_response = client.post("/elderly/", json={
            "custom_id": 201,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        assignment_response = client.post("/caregiver-assignments/", json={
            "caregiver_id": caregiver_id,
            "elderly_id": elderly_id
        }, headers=auth_headers)
        assignment_id = assignment_response.json()["id"]  # Get the assignment ID

        # Delete assignment
        response = client.delete(f"/caregiver-assignments/{assignment_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["message"] == f"Assignment {assignment_id} deleted successfully"

def test_delete_nonexistent_assignment(setup_database, auth_headers):
    with TestClient(app) as client:
        # Attempt to delete a non-existent assignment
        response = client.delete("/caregiver-assignments/99", headers=auth_headers)  # Non-existent assignment ID
        assert response.status_code == 404
        assert response.json()["detail"] == "Assignment not found"

def test_get_all_assignments_success(setup_database, auth_headers):
    # Add caregiver, elderly, and assignment
    with TestClient(app) as client:
        caregiver_response = client.post("/caregivers/", json={
            "custom_id": 101,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        }, headers=auth_headers)
        caregiver_id = caregiver_response.json()["id"]  # Get the internal ID
        
        elderly_response = client.post("/elderly/", json={
            "custom_id": 201,
            "name": "Alice"
        }, headers=auth_headers)
        elderly_id = elderly_response.json()["id"]  # Get the internal ID
        
        client.post("/caregiver-assignments/", json={
            "caregiver_id": caregiver_id,
            "elderly_id": elderly_id
        }, headers=auth_headers)

        # Retrieve all assignments
        response = client.get("/caregiver-assignments/", headers=auth_headers)
        assert response.status_code == 200
        assignments = response.json()
        assert len(assignments) == 1
        assert assignments[0]["caregiver_id"] == caregiver_id
        assert assignments[0]["elderly_id"] == elderly_id
     
