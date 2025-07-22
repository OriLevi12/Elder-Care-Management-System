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
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache
from services.elderly_service import (
    get_all_elderly_service, 
    add_elderly_service, 
    delete_elderly_service,
    get_elderly_by_id_service,
    add_task_to_elderly_service,
    delete_task_from_elderly_service,
    update_task_status_service,
    add_medication_to_elderly_service,
    get_medications_for_elderly_service,
    delete_medication_from_elderly_service
)

router = APIRouter()

# ==================== ELDERLY CRUD OPERATIONS ====================

@router.post("/", response_model=ElderlySchema)
def add_elderly(elderly: ElderlyCreate, db: Session = Depends(get_db)):
    """
    Create a new elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a new elderly person is added, related caches are cleared.
    
    Args:
        elderly: ElderlyCreate schema containing elderly data
        db: Database session (injected by FastAPI)
        
    Returns:
        ElderlySchema: The created elderly person
        
    Raises:
        HTTPException: If elderly with same ID already exists
    """
    return add_elderly_service(elderly, db)

@router.get("/", response_model=list[ElderlySchema])
def get_all_elderly(db: Session = Depends(get_db)):
    """
    Retrieve all elderly persons.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        list[ElderlySchema]: List of all elderly persons
    """
    return get_all_elderly_service(db)

@router.get("/{elderly_id}", response_model=ElderlySchema)
def get_elderly_by_id(elderly_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific elderly person by ID.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        elderly_id: ID of the elderly person to retrieve
        db: Database session (injected by FastAPI)
        
    Returns:
        ElderlySchema: The elderly person data
        
    Raises:
        HTTPException: If elderly person not found
    """
    return get_elderly_by_id_service(elderly_id, db)

@router.delete("/{elderly_id}")
def delete_elderly(elderly_id: int, db: Session = Depends(get_db)):
    """
    Delete an elderly person by ID.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When an elderly person is deleted, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If elderly person not found
    """
    return delete_elderly_service(elderly_id, db)

# ==================== TASK OPERATIONS ====================

@router.post("/{elderly_id}/tasks", response_model=TaskSchema)
def add_task_to_elderly(elderly_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """
    Add a new task for an elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a new task is added, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person
        task: TaskCreate schema containing task data
        db: Database session (injected by FastAPI)
        
    Returns:
        TaskSchema: The created task
        
    Raises:
        HTTPException: If elderly person not found
    """
    return add_task_to_elderly_service(elderly_id, task, db)

@router.delete("/{elderly_id}/tasks/{task_id}")
def delete_task_from_elderly(elderly_id: int, task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task for an elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a task is deleted, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If task not found
    """
    return delete_task_from_elderly_service(elderly_id, task_id, db)

@router.put("/{elderly_id}/tasks/{task_id}/status", response_model=TaskSchema)
def update_task_status(elderly_id: int, task_id: int, new_status: str, db: Session = Depends(get_db)):
    """
    Update the status of a task for an elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a task status is updated, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to update
        new_status: New status for the task
        db: Database session (injected by FastAPI)
        
    Returns:
        TaskSchema: The updated task
        
    Raises:
        HTTPException: If task not found
    """
    return update_task_status_service(elderly_id, task_id, new_status, db)

# ==================== MEDICATION OPERATIONS ====================

@router.post("/{elderly_id}/medications", response_model=MedicationResponse)
def add_medication_to_elderly(elderly_id: int, medication: MedicationCreate, db: Session = Depends(get_db)):
    """
    Add a new medication for an elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a new medication is added, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person
        medication: MedicationCreate schema containing medication data
        db: Database session (injected by FastAPI)
        
    Returns:
        MedicationResponse: The created medication
        
    Raises:
        HTTPException: If elderly person not found
    """
    return add_medication_to_elderly_service(elderly_id, medication, db)

@router.get("/{elderly_id}/medications", response_model=list[MedicationResponse])
def get_medications_for_elderly(elderly_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all medications for an elderly person.
    
    This endpoint uses Redis caching for improved performance.
    - First request: Data fetched from database and cached
    - Subsequent requests: Data served from Redis cache
    - Cache TTL: 300 seconds (5 minutes)
    
    Args:
        elderly_id: ID of the elderly person
        db: Database session (injected by FastAPI)
        
    Returns:
        list[MedicationResponse]: List of medications for the elderly person
        
    Raises:
        HTTPException: If elderly person not found
    """
    return get_medications_for_elderly_service(elderly_id, db)

@router.delete("/{elderly_id}/medications/{medication_id}")
def delete_medication_from_elderly(elderly_id: int, medication_id: int, db: Session = Depends(get_db)):
    """
    Delete a medication for an elderly person.
    
    This endpoint uses Redis cache invalidation to ensure data consistency.
    When a medication is deleted, related caches are cleared.
    
    Args:
        elderly_id: ID of the elderly person
        medication_id: ID of the medication to delete
        db: Database session (injected by FastAPI)
        
    Returns:
        dict: Success message with medication name
        
    Raises:
        HTTPException: If medication not found
    """
    return delete_medication_from_elderly_service(elderly_id, medication_id, db)
