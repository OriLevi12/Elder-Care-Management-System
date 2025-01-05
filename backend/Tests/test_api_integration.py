import pytest
from httpx import AsyncClient
from main import app
from db.database import Base, engine
from sqlalchemy.orm import sessionmaker

# Create a test database session
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

### Caregiver Tests ###
@pytest.mark.asyncio
async def test_add_caregiver_success(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/caregivers/", json={
            "id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

@pytest.mark.asyncio
async def test_add_existing_caregiver(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/caregivers/", json={
            "id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        })
        response = await client.post("/caregivers/", json={
            "id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        })
        assert response.status_code == 400
        assert response.json()["detail"] == "Caregiver already exists"

@pytest.mark.asyncio
async def test_get_caregivers_success(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/caregivers/", json={
            "id": 1,
            "name": "John Doe",
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        })
        response = await client.get("/caregivers/")
        assert response.status_code == 200
        assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_delete_nonexistent_caregiver(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.delete("/caregivers/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Caregiver not found"

### Elderly Tests ###
@pytest.mark.asyncio
async def test_add_elderly_success(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Alice"

@pytest.mark.asyncio
async def test_add_existing_elderly(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        response = await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        assert response.status_code == 400
        assert response.json()["detail"] == "Elderly with this ID already exists"

@pytest.mark.asyncio
async def test_get_elderly_success(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        response = await client.get("/elderly/")
        assert response.status_code == 200
        assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_add_task_to_elderly_success(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        response = await client.post("/elderly/1/tasks", json={
            "description": "Take medicine",
            "status": "pending"
        })
        assert response.status_code == 200
        assert response.json()["description"] == "Take medicine"

@pytest.mark.asyncio
async def test_add_task_to_nonexistent_elderly(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/elderly/99/tasks", json={
            "description": "Take medicine",
            "status": "pending"
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "Elderly not found"

### Medication Tests ###

@pytest.mark.asyncio
async def test_add_medication_to_elderly_success(setup_database):
    # Add an elderly person first
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        
        # Add a medication for the elderly person
        response = await client.post("/elderly/1/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "Aspirin"

@pytest.mark.asyncio
async def test_add_medication_to_nonexistent_elderly(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Attempt to add medication for a non-existent elderly person
        response = await client.post("/elderly/99/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "Elderly not found"

@pytest.mark.asyncio
async def test_get_medications_for_elderly_success(setup_database):
    # Add an elderly person and medications
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        await client.post("/elderly/1/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        })
        await client.post("/elderly/1/medications", json={
            "name": "Ibuprofen",
            "dosage": "200mg",
            "frequency": "Twice a day"
        })
        
        # Retrieve medications for the elderly person
        response = await client.get("/elderly/1/medications")
        assert response.status_code == 200
        medications = response.json()
        assert len(medications) == 2
        assert medications[0]["name"] == "Aspirin"
        assert medications[1]["name"] == "Ibuprofen"

@pytest.mark.asyncio
async def test_delete_medication_from_elderly_success(setup_database):
    # Add an elderly person and a medication
    async with AsyncClient(base_url="http://localhost:8000") as client:
        await client.post("/elderly/", json={
            "id": 1,
            "name": "Alice"
        })
        await client.post("/elderly/1/medications", json={
            "name": "Aspirin",
            "dosage": "500mg",
            "frequency": "Once a day"
        })
        
        # Delete the medication
        response = await client.delete("/elderly/1/medications/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Medication 'Aspirin' deleted successfully"

@pytest.mark.asyncio
async def test_delete_nonexistent_medication_from_elderly(setup_database):
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Attempt to delete a non-existent medication
        response = await client.delete("/elderly/1/medications/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Medication not found"

     
