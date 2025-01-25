from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.caregiver import Caregiver  
from models.elderly import Elderly 
from models.caregiver_assignments import CaregiverAssignment
from schemas.caregiver_assignment import CaregiverAssignmentCreate, CaregiverAssignmentResponse

router = APIRouter()

@router.post("/", response_model=CaregiverAssignmentResponse)
def create_assignment(assignment: CaregiverAssignmentCreate, db: Session = Depends(get_db)):
    # Verify caregiver exists
    caregiver = db.query(Caregiver).filter(Caregiver.id == assignment.caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    # Verify elderly exists
    elderly = db.query(Elderly).filter(Elderly.id == assignment.elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Check if the assignment already exists
    existing_assignment = (
        db.query(CaregiverAssignment)
        .filter(
            CaregiverAssignment.caregiver_id == assignment.caregiver_id,
            CaregiverAssignment.elderly_id == assignment.elderly_id
        )
        .first()
    )
    if existing_assignment:
        raise HTTPException(
            status_code=400,
            detail="Assignment between this caregiver and elderly already exists"
        )
    
    # Create the assignment
    new_assignment = CaregiverAssignment(caregiver_id=assignment.caregiver_id, elderly_id=assignment.elderly_id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


@router.get("/", response_model=list[CaregiverAssignmentResponse])
def get_all_assignments(db: Session = Depends(get_db)):
    return db.query(CaregiverAssignment).all()

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(CaregiverAssignment).filter(CaregiverAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": f"Assignment {assignment_id} deleted successfully"}
