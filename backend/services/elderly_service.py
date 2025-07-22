from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.elderly import ElderlySchema, ElderlyCreate
from schemas.task import TaskSchema, TaskCreate
from schemas.medication import MedicationCreate, MedicationResponse
from models.elderly import Elderly
from models.task import Task
from models.medication import Medication
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def add_elderly_service(elderly: ElderlyCreate, db: Session) -> ElderlySchema:
    """
    Add a new elderly person to the database with Redis cache invalidation.
    
    Args:
        elderly: ElderlyCreate schema containing elderly data
        db: Database session
        
    Returns:
        ElderlySchema: The created elderly person
        
    Raises:
        HTTPException: If elderly with same ID already exists
    """
    # Check if elderly with same ID already exists
    existing_elderly = db.query(Elderly).filter(Elderly.id == elderly.id).first()
    if existing_elderly:
        raise HTTPException(status_code=400, detail="Elderly with this ID already exists")

    # Create and save new elderly person
    new_elderly = Elderly(id=elderly.id, name=elderly.name)
    db.add(new_elderly)
    db.commit()
    db.refresh(new_elderly)

    # Invalidate related caches to ensure data consistency
    print("🧹 Clearing elderly list cache and specific elderly cache")
    delete_from_cache("elderly_list")  # Clear the list cache
    delete_from_cache(f"elderly_{new_elderly.id}")  # Clear individual cache

    return new_elderly

def get_all_elderly_service(db: Session) -> list[ElderlySchema]:
    """
    Retrieve all elderly persons with Redis caching.
    
    Cache Strategy:
    - Cache key: "elderly_list"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        db: Database session
        
    Returns:
        list[ElderlySchema]: List of all elderly persons
    """
    cache_key = "elderly_list"

    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print("✅ Retrieved elderly list from Redis cache")
        return [ElderlySchema(**e) for e in cached_data]

    # Cache miss - query database
    elderly = db.query(Elderly).all()
    result = [ElderlySchema.from_orm(e) for e in elderly]
    
    # Store result in cache for future requests
    print("📦 Retrieved elderly list from DB and storing in Redis")
    set_in_cache(cache_key, [e.dict() for e in result], ttl=300)

    return result

def get_elderly_by_id_service(elderly_id: int, db: Session) -> ElderlySchema:
    """
    Retrieve a specific elderly person by ID with Redis caching.
    
    Cache Strategy:
    - Cache key: "elderly_{elderly_id}"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        elderly_id: ID of the elderly person to retrieve
        db: Database session
        
    Returns:
        ElderlySchema: The elderly person data
        
    Raises:
        HTTPException: If elderly person not found
    """
    cache_key = f"elderly_{elderly_id}"
    
    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print(f"✅ Retrieved elderly {elderly_id} from Redis cache")
        return ElderlySchema(**cached_data)
    
    # Cache miss - query database
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Convert to schema and cache the result
    result = ElderlySchema.from_orm(elderly)
    print(f"📦 Retrieved elderly {elderly_id} from DB and storing in Redis")
    set_in_cache(cache_key, result.dict(), ttl=300)
    
    return result

def delete_elderly_service(elderly_id: int, db: Session) -> dict:
    """
    Delete an elderly person by ID with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person to delete
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If elderly person not found
    """
    # Check if elderly exists before deletion
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    # Delete from database
    db.delete(elderly)
    db.commit()

    # Invalidate related caches to ensure data consistency
    delete_from_cache("elderly_list")  # Clear the list cache
    delete_from_cache(f"elderly_{elderly_id}")  # Clear individual cache

    return {"message": f"Elderly {elderly_id} deleted successfully"}

# ==================== TASK-RELATED SERVICES ====================

def add_task_to_elderly_service(elderly_id: int, task: TaskCreate, db: Session) -> TaskSchema:
    """
    Add a new task for an elderly person with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person
        task: TaskCreate schema containing task data
        db: Database session
        
    Returns:
        TaskSchema: The created task
        
    Raises:
        HTTPException: If elderly person not found
    """
    # Verify elderly person exists
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    # Create and save new task
    new_task = Task(description=task.description, status=task.status, elderly=elderly)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache(f"tasks_elderly_{elderly_id}")  # Clear tasks cache
    
    return new_task

def delete_task_from_elderly_service(elderly_id: int, task_id: int, db: Session) -> dict:
    """
    Delete a task for an elderly person with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to delete
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If task not found
    """
    # Find and verify task exists
    task = db.query(Task).filter(Task.id == task_id, Task.elderly_id == elderly_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete from database
    db.delete(task)
    db.commit()
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache(f"tasks_elderly_{elderly_id}")  # Clear tasks cache
    
    return {"message": f"Task {task_id} deleted successfully"}

def update_task_status_service(elderly_id: int, task_id: int, new_status: str, db: Session) -> TaskSchema:
    """
    Update the status of a task for an elderly person with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person
        task_id: ID of the task to update
        new_status: New status for the task
        db: Database session
        
    Returns:
        TaskSchema: The updated task
        
    Raises:
        HTTPException: If task not found
    """
    # Find and verify task exists
    task = db.query(Task).filter(Task.id == task_id, Task.elderly_id == elderly_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status
    task.status = new_status
    db.commit()
    db.refresh(task)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache(f"tasks_elderly_{elderly_id}")  # Clear tasks cache
    
    return task

# ==================== MEDICATION-RELATED SERVICES ====================

def add_medication_to_elderly_service(elderly_id: int, medication: MedicationCreate, db: Session) -> MedicationResponse:
    """
    Add a new medication for an elderly person with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person
        medication: MedicationCreate schema containing medication data
        db: Database session
        
    Returns:
        MedicationResponse: The created medication
        
    Raises:
        HTTPException: If elderly person not found
    """
    # Verify elderly person exists
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
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
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache(f"medications_elderly_{elderly_id}")  # Clear medications cache
    
    return new_medication

def get_medications_for_elderly_service(elderly_id: int, db: Session) -> list[MedicationResponse]:
    """
    Retrieve all medications for an elderly person with Redis caching.
    
    Cache Strategy:
    - Cache key: "medications_elderly_{elderly_id}"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        elderly_id: ID of the elderly person
        db: Database session
        
    Returns:
        list[MedicationResponse]: List of medications for the elderly person
        
    Raises:
        HTTPException: If elderly person not found
    """
    cache_key = f"medications_elderly_{elderly_id}"
    
    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print(f"✅ Retrieved medications for elderly {elderly_id} from Redis cache")
        return [MedicationResponse(**m) for m in cached_data]
    
    # Cache miss - query database
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Convert to schema and cache the result
    result = [MedicationResponse.from_orm(m) for m in elderly.medications]
    print(f"📦 Retrieved medications for elderly {elderly_id} from DB and storing in Redis")
    set_in_cache(cache_key, [m.dict() for m in result], ttl=300)
    
    return result

def delete_medication_from_elderly_service(elderly_id: int, medication_id: int, db: Session) -> dict:
    """
    Delete a medication for an elderly person with Redis cache invalidation.
    
    Args:
        elderly_id: ID of the elderly person
        medication_id: ID of the medication to delete
        db: Database session
        
    Returns:
        dict: Success message with medication name
        
    Raises:
        HTTPException: If medication not found
    """
    # Find and verify medication exists
    medication = db.query(Medication).filter(Medication.id == medication_id, Medication.elderly_id == elderly_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    # Store medication name for response message
    medication_name = medication.name
    
    # Delete from database
    db.delete(medication)
    db.commit()
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache(f"medications_elderly_{elderly_id}")  # Clear medications cache
    
    return {"message": f"Medication '{medication_name}' deleted successfully"}
