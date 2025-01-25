from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.elderly import Elderly
from models.task import Task
from models.medication import Medication
from models.caregiver_assignments import CaregiverAssignment
from schemas.medication import MedicationCreate, MedicationResponse
from schemas.elderly import ElderlySchema, ElderlyCreate
from schemas.task import TaskSchema, TaskCreate
from db.database import get_db

router = APIRouter()

# Create a new elderly person
@router.post("/", response_model=ElderlySchema)
def add_elderly(elderly: ElderlyCreate, db: Session = Depends(get_db)):
    existing_elderly = db.query(Elderly).filter(Elderly.id == elderly.id).first()
    if existing_elderly:
        raise HTTPException(status_code=400, detail="Elderly with this ID already exists")

    new_elderly = Elderly(id=elderly.id, name=elderly.name)
    db.add(new_elderly)
    db.commit()
    db.refresh(new_elderly)
    return new_elderly

# Get all elderly persons
@router.get("/", response_model=list[ElderlySchema])
def get_all_elderly(db: Session = Depends(get_db)):
    return db.query(Elderly).all()

# Get a specific elderly person by ID
@router.get("/{elderly_id}", response_model=ElderlySchema)
def get_elderly_by_id(elderly_id: int, db: Session = Depends(get_db)):
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    return elderly

# Delete an elderly person by ID
@router.delete("/{elderly_id}")
def delete_elderly(elderly_id: int, db: Session = Depends(get_db)):
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    db.delete(elderly)
    db.commit()
    return {"message": f"Elderly {elderly_id} deleted successfully"}

# Add a new task for an elderly person
@router.post("/{elderly_id}/tasks", response_model=TaskSchema)
def add_task_to_elderly(elderly_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    new_task = Task(description=task.description, status=task.status, elderly=elderly)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Delete a task by ID for a specific elderly person
@router.delete("/{elderly_id}/tasks/{task_id}")
def delete_task_from_elderly(elderly_id: int, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.elderly_id == elderly_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}

# Update the status of a task for a specific elderly person
@router.put("/{elderly_id}/tasks/{task_id}/status", response_model=TaskSchema)
def update_task_status(elderly_id: int, task_id: int, new_status: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.elderly_id == elderly_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = new_status
    db.commit()
    db.refresh(task)
    return task

# Add a medication for an elderly person
@router.post("/{elderly_id}/medications", response_model=MedicationResponse)
def add_medication_to_elderly(elderly_id: int, medication: MedicationCreate, db: Session = Depends(get_db)):
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    new_medication = Medication(
        name=medication.name,
        dosage=medication.dosage,
        frequency=medication.frequency,
        elderly=elderly
    )
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    return new_medication

# Get all medications for an elderly person
@router.get("/{elderly_id}/medications", response_model=list[MedicationResponse])
def get_medications_for_elderly(elderly_id: int, db: Session = Depends(get_db)):
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    return elderly.medications

# Delete a medication for an elderly person
@router.delete("/{elderly_id}/medications/{medication_id}")
def delete_medication_from_elderly(elderly_id: int, medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(Medication).filter(Medication.id == medication_id, Medication.elderly_id == elderly_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    db.delete(medication)
    db.commit()
    return {"message": f"Medication '{medication.name}' deleted successfully"}