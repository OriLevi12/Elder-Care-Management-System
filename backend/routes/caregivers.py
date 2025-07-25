from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from models.caregiver import Caregiver
from models.caregiver_assignments import CaregiverAssignment
from schemas.caregiver import CaregiverCreate, CaregiverUpdateSalary, CaregiverResponse
from db.database import get_db
from utils.pdf_generator import generate_caregiver_pdf
from services.caregiver_service import (
    add_caregiver_service,
    get_all_caregivers_service,
    get_caregiver_by_id_service,
    update_caregiver_salary_service,
    generate_caregiver_pdf_service,
    delete_caregiver_service
)

router = APIRouter()

# ==================== CAREGIVER CRUD OPERATIONS ====================

@router.post("/", response_model=CaregiverResponse)
def add_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    """
    Create a new caregiver.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a new caregiver is added, related caches are cleared.
    
    Args:
        caregiver: CaregiverCreate schema containing caregiver data
        db: Database session (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The created caregiver
        
    Raises:
        HTTPException: If caregiver with same ID already exists
    """
    return add_caregiver_service(caregiver, db)

@router.get("/", response_model=list[CaregiverResponse])
def get_caregivers(db: Session = Depends(get_db)):
    """
    Retrieve all caregivers.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        list[CaregiverResponse]: List of all caregivers
    """
    return get_all_caregivers_service(db)

@router.get("/{caregiver_id}", response_model=CaregiverResponse)
def get_caregiver_by_id(caregiver_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific caregiver by ID.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        caregiver_id: ID of the caregiver to retrieve
        db: Database session (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The caregiver data
        
    Raises:
        HTTPException: If caregiver not found
    """
    return get_caregiver_by_id_service(caregiver_id, db)

@router.put("/{id}/update-salary", response_model=CaregiverResponse)
def update_salary(id: int, salary_update: CaregiverUpdateSalary, db: Session = Depends(get_db)):
    """
    Update caregiver salary information.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When salary information is updated, related caches are cleared.
    
    Args:
        id: ID of the caregiver to update
        salary_update: CaregiverUpdateSalary schema containing salary data
        db: Database session (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The updated caregiver
        
    Raises:
        HTTPException: If caregiver not found
    """
    return update_caregiver_salary_service(id, salary_update, db)

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(id: int, db: Session = Depends(get_db)):
    """
    Generate PDF for a specific caregiver.
    
    This endpoint uses Redis caching for improved performance.
    Caregiver data is retrieved from cache if available.
    
    Args:
        id: ID of the caregiver
        db: Database session (injected by FastAPI)
        
    Returns:
        FileResponse: The generated PDF file
        
    Raises:
        HTTPException: If caregiver not found
    """
    filename = generate_caregiver_pdf_service(id, db)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.delete("/{id}")
def delete_caregiver(id: int, db: Session = Depends(get_db)):
    """
    Delete a caregiver by ID.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a caregiver is deleted, related caches are cleared.
    
    Args:
        id: ID of the caregiver to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If caregiver not found
    """
    return delete_caregiver_service(id, db)
