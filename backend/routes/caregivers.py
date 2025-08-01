from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from models.caregiver import Caregiver
from models.caregiver_assignments import CaregiverAssignment
from models.user import User
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
from services.auth_service import get_current_user

router = APIRouter()

# ==================== CAREGIVER CRUD OPERATIONS ====================

@router.post("/", response_model=CaregiverResponse)
def add_caregiver(
    caregiver: CaregiverCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new caregiver.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a new caregiver is added, related caches are cleared.
    
    Args:
        caregiver: CaregiverCreate schema containing caregiver data
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The created caregiver
        
    Raises:
        HTTPException: If caregiver with same ID already exists
    """
    return add_caregiver_service(caregiver, current_user.id, db)

@router.get("/", response_model=list[CaregiverResponse])
def get_caregivers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all caregivers for the current user.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        list[CaregiverResponse]: List of all caregivers for the current user
    """
    return get_all_caregivers_service(current_user.id, db)

@router.get("/{caregiver_id}", response_model=CaregiverResponse)
def get_caregiver_by_id(
    caregiver_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific caregiver by ID (for current user only).
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        caregiver_id: ID of the caregiver to retrieve
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The caregiver data
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to current user
    """
    return get_caregiver_by_id_service(caregiver_id, current_user.id, db)

@router.put("/{id}/update-salary", response_model=CaregiverResponse)
def update_salary(
    id: int, 
    salary_update: CaregiverUpdateSalary, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update caregiver salary information (for current user only).
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When salary information is updated, related caches are cleared.
    
    Args:
        id: ID of the caregiver to update
        salary_update: CaregiverUpdateSalary schema containing salary data
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        CaregiverResponse: The updated caregiver
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to current user
    """
    return update_caregiver_salary_service(id, salary_update, current_user.id, db)

@router.get("/{id}/generate-pdf")
def generate_pdf_for_caregiver(
    id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate PDF for a specific caregiver (for current user only).
    
    This endpoint uses Redis caching for improved performance.
    Caregiver data is retrieved from cache if available.
    
    Args:
        id: ID of the caregiver
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        FileResponse: The generated PDF file
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to current user
    """
    filename = generate_caregiver_pdf_service(id, current_user.id, db)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.delete("/{id}")
def delete_caregiver(
    id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a caregiver by ID (for current user only).
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a caregiver is deleted, related caches are cleared.
    
    Args:
        id: ID of the caregiver to delete
        db: Database session (injected by FastAPI)
        current_user: Current authenticated user (injected by FastAPI)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to current user
    """
    return delete_caregiver_service(id, current_user.id, db)
