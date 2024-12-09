from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.caregiver import Caregiver


router = APIRouter()

@router.post("/")
def add_caregiver(name: str, id: int, bank_name: str, bank_account: str, branch_number: str):
    try:
        Caregiver.add(name, id, bank_name, bank_account, branch_number)
        return {"message": f"Caregiver {name} added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_caregivers():
    return {"caregivers": Caregiver.get_all()}

@router.put("/{id}/update-salary")
def put_salary(id: int, salary_price: float, salary_amount: int, saturday_price: float, saturday_amount: int,
               allowance_price: float, allowance_amount: int):
    try:
        caregiver = Caregiver.get(id)
        caregiver.update_salary(salary_price, salary_amount, saturday_price, saturday_amount, allowance_price, allowance_amount)
        return {"message": f"Salary updated for caregiver {id}", "total_bank": caregiver.total_bank}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(id: int):
    try:
        caregiver = Caregiver.get(id)
        filename = caregiver.generate_pdf()
        return FileResponse(filename, media_type="application/pdf", filename=filename)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}")
def delete_caregiver(id: int):
    try:
        caregiver = Caregiver.delete(id)
        return {"message": f"Caregiver {caregiver.name} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

