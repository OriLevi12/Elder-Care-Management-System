from fastapi import APIRouter, HTTPException
from models.medication import Medication

router = APIRouter()

medications = []
medication_id = 1

@router.post("/")
def add_medication(name: str, dosage: str, frequency: str):
    global medication_id

    if any(med.name == name for med in medications):
        raise HTTPException(status_code=400, detail="Medication already exists")

    new_medication = Medication(id=medication_id, name=name, dosage=dosage, frequency=frequency)
    medications.append(new_medication)
    medication_id += 1

    return {"message": f"Medication '{name}' added successfully", "medication": new_medication.dict()}

@router.get("/")
def get_medications():
    return {"medications": [med.dict() for med in medications]}

@router.delete("/{id}")
def delete_medication(id: int):
    for i, med in enumerate(medications):
        if med.id == id:
            deleted_medication = medications.pop(i)
            return {"message": f"Medication '{deleted_medication.name}' deleted successfully"}

    raise HTTPException(status_code=404, detail="Medication not found")

