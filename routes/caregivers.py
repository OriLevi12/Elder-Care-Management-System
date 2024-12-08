from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.caregiver import Caregiver
from utils.pdf_generator import generate_caregiver_pdf


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

@router.put("/{id}/update-all")
def update_all(
    id: int,
    salary_price: float,
    salary_amount: int,
    saturday_price: float,
    saturday_amount: int,
    allowance_price: float,
    allowance_amount: int
):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    caregivers[id].update_all(salary_price, salary_amount, saturday_price, saturday_amount, allowance_price, allowance_amount)

    return {
        "message": f"All details updated for caregiver {id}",
        "total_bank": caregivers[id].total_bank
    }

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(id: int):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    filename = generate_caregiver_pdf(caregivers[id])
    return FileResponse(filename, media_type="application/pdf", filename=filename)
