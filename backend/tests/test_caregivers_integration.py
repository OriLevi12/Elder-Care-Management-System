import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_add_caregiver():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/caregivers/", params={
            "name": "John Doe",
            "id": 1,
            "bank_name": "Bank A",
            "bank_account": "12345",
            "branch_number": "001"
        })
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["message"] == "Caregiver John Doe added successfully"
        assert "caregiver" in response_json


@pytest.mark.asyncio
async def test_delete_nonexistent_caregiver():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.delete("/caregivers/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Caregiver not found"}


@pytest.mark.asyncio
async def test_add_caregiver_invalid_data():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/caregivers/", params={
            "name": "Invalid Caregiver",
        })
        assert response.status_code == 422
        assert all(item["msg"] == "Field required" for item in response.json()["detail"])

@pytest.mark.asyncio
async def test_get_caregivers():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/caregivers/")
        assert response.status_code == 200
        assert len(response.json()["caregivers"]) > 0

@pytest.mark.asyncio
async def test_delete_caregiver():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.delete("/caregivers/1")
        assert response.status_code == 200
        assert response.json() == {"message": "Caregiver John Doe deleted successfully"}
