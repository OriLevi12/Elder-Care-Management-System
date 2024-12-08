from fastapi import APIRouter, HTTPException
from models.caregiver import Caregiver

router = APIRouter()

caregivers = {}

@router.post("/")
def add_caregiver(name: str, id: int, bank_name: str, bank_account: str, branch_number: str):
    if id in caregivers:
        raise HTTPException(status_code=400, detail="Caregiver already exists")
    caregivers[id] = Caregiver(name, id, bank_name, bank_account, branch_number)
    return {"message": f"Caregiver {name} added successfully"}

@router.get("/")
def get_caregivers():
    return {"caregivers": list(caregivers.values())}

@router.post("/{id}/tasks")
def add_task_to_caregiver(id: int, task: str):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    caregivers[id].add_task(task)
    return {"message": f"Task '{task}' added for caregiver {id}"}
