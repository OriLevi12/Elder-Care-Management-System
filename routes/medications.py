from fastapi import APIRouter, HTTPException
from models.medication import Medication

router = APIRouter()

@router.post("/")
def add_medication(name: str, dosage: str, frequency: str):
    medication = Medication.add_medication(name, dosage, frequency)
    if medication is None:
        raise HTTPException(status_code=400, detail="Medication already exists")
    return {"message": f"Medication '{name}' added successfully", "medication": medication.__dict__}

@router.get("/")
def get_medications():
    return {"medications": Medication.get_all_medications()}

@router.delete("/{id}")
def delete_medication(id: int):
    medication = Medication.delete_medication(id)
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": f"Medication '{medication.name}' deleted successfully"}
