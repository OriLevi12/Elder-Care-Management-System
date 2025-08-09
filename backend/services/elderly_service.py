from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.elderly import ElderlySchema, ElderlyCreate
from schemas.task import TaskSchema, TaskCreate
from schemas.medication import MedicationCreate, MedicationResponse
from models.elderly import Elderly
from models.task import Task
from models.medication import Medication
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def add_elderly_service(elderly: ElderlyCreate, user_id: int, db: Session) -> ElderlySchema:
    """
    Add a new elderly person to the database with Redis cache invalidation.
    Automatically assigns the elderly to the current user for data isolation.
    
    Args:
        elderly: ElderlyCreate schema containing elderly data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        ElderlySchema: The created elderly person
        
    Raises:
        HTTPException: If elderly with same custom_id already exists for this user
    """
    # Check if elderly with same custom_id already exists for THIS USER
    existing_elderly = db.query(Elderly).filter(
        Elderly.custom_id == elderly.custom_id, 
        Elderly.user_id == user_id
    ).first()
    if existing_elderly:
        raise HTTPException(status_code=400, detail="Elderly with this ID already exists for this user")

    # Create and save new elderly person with user_id
    new_elderly = Elderly(custom_id=elderly.custom_id, name=elderly.name, user_id=user_id)
    db.add(new_elderly)
    db.commit()
    db.refresh(new_elderly)

    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific list cache
    delete_from_cache(f"user_{user_id}_elderly_{new_elderly.id}")  # Clear user-specific individual cache

    return new_elderly

def get_all_elderly_service(user_id: int, db: Session) -> list[ElderlySchema]:
    """
    Retrieve all elderly persons for a specific user with Redis caching.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_elderly_list"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        list[ElderlySchema]: List of elderly persons for the current user
    """
    cache_key = f"user_{user_id}_elderly_list"

    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return [ElderlySchema(**e) for e in cached_data]

    # Cache miss - query database with user filter
    elderly = db.query(Elderly).filter(Elderly.user_id == user_id).all()
    result = [ElderlySchema.from_orm(e) for e in elderly]
    
    # Store result in cache for future requests
    set_in_cache(cache_key, [e.dict() for e in result], ttl=300)

    return result

def get_elderly_by_id_service(elderly_id: int, user_id: int, db: Session) -> ElderlySchema:
    """
    Retrieve a specific elderly person by ID for a specific user with Redis caching.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_elderly_{elderly_id}"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        elderly_id: ID of the elderly person to retrieve
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        ElderlySchema: The elderly person data
        
    Raises:
        HTTPException: If elderly person not found or doesn't belong to user
    """
    cache_key = f"user_{user_id}_elderly_{elderly_id}"
    
    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return ElderlySchema(**cached_data)
    
    # Cache miss - query database with user filter
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Convert to schema and cache the result
    result = ElderlySchema.from_orm(elderly)
    set_in_cache(cache_key, result.dict(), ttl=300)
    
    return result

def delete_elderly_service(elderly_id: int, user_id: int, db: Session) -> dict:
    """
    Delete an elderly person by ID for a specific user with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person to delete
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If elderly person not found or doesn't belong to user
    """
    # Check if elderly exists and belongs to the user
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    # Delete from database
    db.delete(elderly)
    db.commit()

    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific list cache
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific individual cache

    return {"message": f"Elderly {elderly_id} deleted successfully"}

# ==================== TASK-RELATED SERVICES ====================

def add_task_to_elderly_service(elderly_id: int, task: TaskCreate, user_id: int, db: Session) -> TaskSchema:
    """
    Add a new task for an elderly person with Redis cache invalidation.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Args:
        elderly_id: ID of the elderly person
        task: TaskCreate schema containing task data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        TaskSchema: The created task
        
    Raises:
        HTTPException: If elderly person not found or doesn't belong to user
    """
    # Verify elderly person exists and belongs to the user
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    # Create and save new task
    new_task = Task(description=task.description, status=task.status, elderly=elderly)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    
    return new_task

def delete_task_from_elderly_service(elderly_id: int, task_id: int, user_id: int, db: Session) -> dict:
    """
    Delete a task for an elderly person with Redis cache invalidation.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to delete
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If task not found or elderly doesn't belong to user
    """
    # Find and verify task exists and elderly belongs to user
    task = db.query(Task).join(Elderly).filter(
        Task.id == task_id, 
        Task.elderly_id == elderly_id,
        Elderly.user_id == user_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete from database
    db.delete(task)
    db.commit()
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    
    return {"message": f"Task {task_id} deleted successfully"}

def update_task_status_service(elderly_id: int, task_id: int, new_status: str, user_id: int, db: Session) -> TaskSchema:
    """
    Update the status of a task for an elderly person with Redis cache invalidation.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to update
        new_status: New status for the task
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        TaskSchema: The updated task
        
    Raises:
        HTTPException: If task not found or elderly doesn't belong to user
    """
    # Find and verify task exists and elderly belongs to user
    task = db.query(Task).join(Elderly).filter(
        Task.id == task_id, 
        Task.elderly_id == elderly_id,
        Elderly.user_id == user_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status
    task.status = new_status
    db.commit()
    db.refresh(task)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    
    return task

# ==================== MEDICATION-RELATED SERVICES ====================

def add_medication_to_elderly_service(elderly_id: int, medication: MedicationCreate, user_id: int, db: Session) -> MedicationResponse:
    """
    Add a new medication for an elderly person with Redis cache invalidation.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Args:
        elderly_id: ID of the elderly person
        medication: MedicationCreate schema containing medication data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        MedicationResponse: The created medication
        
    Raises:
        HTTPException: If elderly person not found or doesn't belong to user
    """
    # Verify elderly person exists and belongs to the user
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    # Create and save new medication
    new_medication = Medication(
        name=medication.name,
        dosage=medication.dosage,
        frequency=medication.frequency,
        elderly=elderly
    )
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    delete_from_cache(f"user_{user_id}_medications_elderly_{elderly_id}")  # Clear user-specific medications cache
    
    return new_medication

def get_medications_for_elderly_service(elderly_id: int, user_id: int, db: Session) -> list[MedicationResponse]:
    """
    Retrieve all medications for an elderly person with Redis caching.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_medications_elderly_{elderly_id}"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        elderly_id: ID of the elderly person
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        list[MedicationResponse]: List of medications for the elderly person
        
    Raises:
        HTTPException: If elderly person not found or doesn't belong to user
    """
    cache_key = f"user_{user_id}_medications_elderly_{elderly_id}"
    
    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return [MedicationResponse(**m) for m in cached_data]
    
    # Cache miss - query database with user filter
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Convert to schema and cache the result
    result = [MedicationResponse.from_orm(m) for m in elderly.medications]
    set_in_cache(cache_key, [m.dict() for c in result], ttl=300)
    
    return result

def delete_medication_from_elderly_service(elderly_id: int, medication_id: int, user_id: int, db: Session) -> dict:
    """
    Delete a medication for an elderly person with Redis cache invalidation.
    Ensures the elderly person belongs to the current user for data isolation.
    
    Args:
        elderly_id: ID of the elderly person
        medication_id: ID of the medication to delete
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        dict: Success message with medication name
        
    Raises:
        HTTPException: If medication not found or elderly doesn't belong to user
    """
    # Find and verify medication exists and elderly belongs to user
    medication = db.query(Medication).join(Elderly).filter(
        Medication.id == medication_id, 
        Medication.elderly_id == elderly_id,
        Elderly.user_id == user_id
    ).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    # Store medication name for response message
    medication_name = medication.name
    
    # Delete from database
    db.delete(medication)
    db.commit()
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    delete_from_cache(f"user_{user_id}_medications_elderly_{elderly_id}")  # Clear user-specific medications cache
    
    return {"message": f"Medication '{medication_name}' deleted successfully"}
