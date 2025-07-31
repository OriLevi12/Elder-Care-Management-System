from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.caregiver import CaregiverResponse, CaregiverCreate, CaregiverUpdateSalary
from models.caregiver import Caregiver
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache
from utils.pdf_generator import generate_caregiver_pdf

def add_caregiver_service(caregiver: CaregiverCreate, user_id: int, db: Session) -> CaregiverResponse:
    """
    Add a new caregiver to the database with Redis cache invalidation.
    Automatically assigns the caregiver to the current user for data isolation.
    
    Args:
        caregiver: CaregiverCreate schema containing caregiver data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        CaregiverResponse: The created caregiver
        
    Raises:
        HTTPException: If caregiver with same ID already exists for this user
    """
    # Check if caregiver with same ID already exists for THIS USER
    existing_caregiver = db.query(Caregiver).filter(
        Caregiver.id == caregiver.id, 
        Caregiver.user_id == user_id
    ).first()
    if existing_caregiver:
        raise HTTPException(status_code=400, detail="Caregiver with this ID already exists for this user")

    # Create and save new caregiver with user_id
    new_caregiver = Caregiver(
        id=caregiver.id,
        name=caregiver.name,
        bank_name=caregiver.bank_name,
        bank_account=caregiver.bank_account,
        branch_number=caregiver.branch_number,
        user_id=user_id
    )
    db.add(new_caregiver)
    db.commit()
    db.refresh(new_caregiver)

    # Invalidate related caches to ensure data consistency
    print("🧹 Clearing caregiver list cache and specific caregiver cache")
    delete_from_cache(f"user_{user_id}_caregiver_list")  # Clear user-specific list cache
    delete_from_cache(f"user_{user_id}_caregiver_{new_caregiver.id}")  # Clear user-specific individual cache

    return new_caregiver

def get_all_caregivers_service(user_id: int, db: Session) -> list[CaregiverResponse]:
    """
    Retrieve all caregivers for a specific user with Redis caching.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_caregiver_list"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        list[CaregiverResponse]: List of caregivers for the current user
    """
    cache_key = f"user_{user_id}_caregiver_list"

    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print(f"✅ Retrieved caregiver list for user {user_id} from Redis cache")
        return [CaregiverResponse(**c) for c in cached_data]

    # Cache miss - query database with user filter
    caregivers = db.query(Caregiver).filter(Caregiver.user_id == user_id).all()
    result = [CaregiverResponse.from_orm(c) for c in caregivers]
    
    # Store result in cache for future requests
    print(f"📦 Retrieved caregiver list for user {user_id} from DB and storing in Redis")
    set_in_cache(cache_key, [c.dict() for c in result], ttl=300)

    return result

def get_caregiver_by_id_service(caregiver_id: int, user_id: int, db: Session) -> CaregiverResponse:
    """
    Retrieve a specific caregiver by ID for a specific user with Redis caching.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_caregiver_{caregiver_id}"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        caregiver_id: ID of the caregiver to retrieve
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        CaregiverResponse: The caregiver data
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to user
    """
    cache_key = f"user_{user_id}_caregiver_{caregiver_id}"
    
    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print(f"✅ Retrieved caregiver {caregiver_id} for user {user_id} from Redis cache")
        return CaregiverResponse(**cached_data)
    
    # Cache miss - query database with user filter
    caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver_id, Caregiver.user_id == user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    # Convert to schema and cache the result
    result = CaregiverResponse.from_orm(caregiver)
    print(f"📦 Retrieved caregiver {caregiver_id} for user {user_id} from DB and storing in Redis")
    set_in_cache(cache_key, result.dict(), ttl=300)
    
    return result

def update_caregiver_salary_service(caregiver_id: int, salary_update: CaregiverUpdateSalary, user_id: int, db: Session) -> CaregiverResponse:
    """
    Update caregiver salary information with Redis cache invalidation.
    Ensures the caregiver belongs to the current user for data isolation.
    
    Args:
        caregiver_id: ID of the caregiver to update
        salary_update: CaregiverUpdateSalary schema containing salary data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        CaregiverResponse: The updated caregiver
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to user
    """
    # Find and verify caregiver exists and belongs to the user
    caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver_id, Caregiver.user_id == user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    # Update salary information
    caregiver.salary = {
        "price": salary_update.salary_price,
        "amount": salary_update.salary_amount,
        "total": salary_update.salary_price * salary_update.salary_amount,
    }
    caregiver.saturday = {
        "price": salary_update.saturday_price,
        "amount": salary_update.saturday_amount,
        "total": salary_update.saturday_price * salary_update.saturday_amount,
    }
    caregiver.allowance = {
        "price": salary_update.allowance_price,
        "amount": salary_update.allowance_amount,
        "total": salary_update.allowance_price * salary_update.allowance_amount,
    }
    caregiver.total_bank = (
        caregiver.salary["total"] +
        caregiver.saturday["total"] +
        caregiver.allowance["total"]
    )
    
    # Save changes to database
    db.commit()
    db.refresh(caregiver)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_caregiver_list")  # Clear user-specific list cache
    delete_from_cache(f"user_{user_id}_caregiver_{caregiver_id}")  # Clear user-specific individual cache
    
    return caregiver

def generate_caregiver_pdf_service(caregiver_id: int, user_id: int, db: Session) -> str:
    """
    Generate PDF for a specific caregiver with Redis cache check.
    Ensures the caregiver belongs to the current user for data isolation.
    
    Args:
        caregiver_id: ID of the caregiver
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        str: Path to the generated PDF file
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to user
    """
    # Get caregiver data (this will use cache if available and filter by user)
    caregiver = get_caregiver_by_id_service(caregiver_id, user_id, db)
    
    # Generate PDF using the utility function
    filename = generate_caregiver_pdf(caregiver)
    return filename

def delete_caregiver_service(caregiver_id: int, user_id: int, db: Session) -> dict:
    """
    Delete a caregiver by ID for a specific user with Redis cache invalidation.
    
    Args:
        caregiver_id: ID of the caregiver to delete
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If caregiver not found or doesn't belong to user
    """
    # Check if caregiver exists and belongs to the user
    caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver_id, Caregiver.user_id == user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    # Delete from database
    db.delete(caregiver)
    db.commit()

    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_caregiver_list")  # Clear user-specific list cache
    delete_from_cache(f"user_{user_id}_caregiver_{caregiver_id}")  # Clear user-specific individual cache

    return {"message": f"Caregiver {caregiver_id} deleted successfully"}
