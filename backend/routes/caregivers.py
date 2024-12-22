from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from models.caregiver import Caregiver
from schemas.caregiver import CaregiverCreate, CaregiverUpdateSalary, CaregiverResponse
from db.database import get_db
from utils.pdf_generator import generate_caregiver_pdf

router = APIRouter()

@router.post("/", response_model=CaregiverResponse)
def add_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    existing_caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver.id).first()
    if existing_caregiver:
        raise HTTPException(status_code=400, detail="Caregiver already exists")

    new_caregiver = Caregiver(
        id=caregiver.id,
        name=caregiver.name,
        bank_name=caregiver.bank_name,
        bank_account=caregiver.bank_account,
        branch_number=caregiver.branch_number,
    )
    db.add(new_caregiver)
    db.commit()
    db.refresh(new_caregiver)
    return new_caregiver

@router.get("/", response_model=list[CaregiverResponse])
def get_caregivers(db: Session = Depends(get_db)):
    return db.query(Caregiver).all()

@router.put("/{id}/update-salary", response_model=CaregiverResponse)
def update_salary(id: int, salary_update: CaregiverUpdateSalary, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.id == id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    caregiver.salary = {
        "price": salary_update.salary_price,
        "amount": salary_update.salary_amount,
        "total": salary_update.salary_price * salary_update.salary_amount,
    }
    caregiver.saturday = {
        "price": salary_update.saturday_price,
        "amount": salary_update.saturday_amount,
        "total": salary_update.saturday_price * salary_update.saturday_amount,
    }
    caregiver.allowance = {
        "price": salary_update.allowance_price,
        "amount": salary_update.allowance_amount,
        "total": salary_update.allowance_price * salary_update.allowance_amount,
    }
    caregiver.total_bank = (
        caregiver.salary["total"] +
        caregiver.saturday["total"] +
        caregiver.allowance["total"]
    )
    db.commit()
    db.refresh(caregiver)
    return caregiver

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.id == id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    filename = generate_caregiver_pdf(caregiver)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.delete("/{id}")
def delete_caregiver(id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.id == id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    db.delete(caregiver)
    db.commit()
    return {"message": f"Caregiver {id} deleted successfully"}
