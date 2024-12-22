from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.medication import Medication
from db.database import get_db
from schemas.medication import MedicationCreate, MedicationResponse

router = APIRouter()

@router.post("/", response_model=MedicationResponse)
def create_medication(medication: MedicationCreate, db: Session = Depends(get_db)):
    db_medication = Medication(name=medication.name, dosage=medication.dosage, frequency=medication.frequency)
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.get("/", response_model=list[MedicationResponse])
def get_medications(db: Session = Depends(get_db)):
    return db.query(Medication).all()

@router.delete("/{medication_id}")
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    db.delete(medication)
    db.commit()
    return {"message": f"Medication '{medication.name}' deleted successfully"}
