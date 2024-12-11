from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.caregiver import Caregiver
from typing import Dict

router = APIRouter()

# Dictionary to store caregivers
caregivers: Dict[int, Caregiver] = {}

@router.post("/")
def add_caregiver(name: str, id: int, bank_name: str, bank_account: str, branch_number: str):
    if id in caregivers:
        raise HTTPException(status_code=400, detail="Caregiver already exists")
    
    caregiver = Caregiver(name=name, id=id, bank_name=bank_name, bank_account=bank_account, branch_number=branch_number)
    caregivers[id] = caregiver
    return {"message": f"Caregiver {name} added successfully", "caregiver": caregiver.dict()}

@router.get("/")
def get_caregivers():
    return {"caregivers": [caregiver.dict() for caregiver in caregivers.values()]}

@router.put("/{id}/update-salary")
def put_salary(id: int, salary_price: float, salary_amount: int, saturday_price: float, saturday_amount: int,
               allowance_price: float, allowance_amount: int):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    caregiver = caregivers[id]
    caregiver.update_salary(salary_price, salary_amount, saturday_price, saturday_amount, allowance_price, allowance_amount)
    return {"message": f"Salary updated for caregiver {id}", "total_bank": caregiver.total_bank}

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(id: int):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    caregiver = caregivers[id]
    filename = caregiver.generate_pdf()
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.delete("/{id}")
def delete_caregiver(id: int):
    if id not in caregivers:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    caregiver = caregivers.pop(id)
    return {"message": f"Caregiver {caregiver.name} deleted successfully"}
