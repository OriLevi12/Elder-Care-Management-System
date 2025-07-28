from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.caregiver import Caregiver  
from models.elderly import Elderly 
from models.caregiver_assignments import CaregiverAssignment
from schemas.caregiver_assignment import CaregiverAssignmentCreate, CaregiverAssignmentResponse
from services.caregiver_assignment_service import (
    create_assignment_service,
    get_all_assignments_service,
    delete_assignment_service
)

router = APIRouter()

# ==================== CAREGIVER ASSIGNMENT OPERATIONS ====================

@router.post("/", response_model=CaregiverAssignmentResponse)
def create_assignment(assignment: CaregiverAssignmentCreate, db: Session = Depends(get_db)):
    """
    Create a new caregiver assignment.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When an assignment is created, both caregiver and elderly caches are cleared.
    
    Args:
        assignment: CaregiverAssignmentCreate schema containing assignment data
        db: Database session (injected by FastAPI)
        
    Returns:
        CaregiverAssignmentResponse: The created assignment
        
    Raises:
        HTTPException: If caregiver or elderly not found, or assignment already exists
    """
    return create_assignment_service(assignment, db)

@router.get("/", response_model=list[CaregiverAssignmentResponse])
def get_all_assignments(db: Session = Depends(get_db)):
    """
    Retrieve all caregiver assignments.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        list[CaregiverAssignmentResponse]: List of all assignments
    """
    return get_all_assignments_service(db)

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Delete a caregiver assignment.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When an assignment is deleted, both caregiver and elderly caches are cleared.
    
    Args:
        assignment_id: ID of the assignment to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If assignment not found
    """
    return delete_assignment_service(assignment_id, db)
