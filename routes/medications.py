from fastapi import APIRouter, HTTPException
from models.medication import Medication

router = APIRouter()

medications = []
medication_id = 1

@router.post("/")
def add_medication(name: str, dosage: str, frequency: str):
    global medication_id
    medication = Medication(medication_id, name, dosage, frequency)
    medications.append(medication)
    medication_id += 1
    return {"message": f"Medication {name} added successfully"}

@router.get("/")
def get_medications():
    return {"medications": medications}
