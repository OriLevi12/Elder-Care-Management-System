from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.caregiver_assignment import CaregiverAssignmentCreate, CaregiverAssignmentResponse
from models.caregiver import Caregiver
from models.elderly import Elderly
from models.caregiver_assignments import CaregiverAssignment
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def create_assignment_service(assignment: CaregiverAssignmentCreate, user_id: int, db: Session) -> CaregiverAssignmentResponse:
    """
    Create a new caregiver assignment with Redis cache invalidation.
    Automatically assigns the assignment to the current user for data isolation.
    
    This function clears both caregiver and elderly caches since assignments
    affect both entities' data.
    
    Args:
        assignment: CaregiverAssignmentCreate schema containing assignment data
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        CaregiverAssignmentResponse: The created assignment
        
    Raises:
        HTTPException: If caregiver or elderly not found, or assignment already exists for this user
    """
    # Verify caregiver exists and belongs to the user
    caregiver = db.query(Caregiver).filter(Caregiver.id == assignment.caregiver_id, Caregiver.user_id == user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    # Verify elderly exists and belongs to the user
    elderly = db.query(Elderly).filter(Elderly.id == assignment.elderly_id, Elderly.user_id == user_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")
    
    # Check if the assignment already exists for THIS USER
    existing_assignment = (
        db.query(CaregiverAssignment)
        .filter(
            CaregiverAssignment.caregiver_id == assignment.caregiver_id,
            CaregiverAssignment.elderly_id == assignment.elderly_id,
            CaregiverAssignment.user_id == user_id
        )
        .first()
    )
    if existing_assignment:
        raise HTTPException(
            status_code=400,
            detail="Assignment between this caregiver and elderly already exists for this user"
        )
    
    # Create the assignment with user_id
    new_assignment = CaregiverAssignment(
        caregiver_id=assignment.caregiver_id, 
        elderly_id=assignment.elderly_id,
        user_id=user_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_caregiver_{assignment.caregiver_id}")  # Clear user-specific caregiver cache
    delete_from_cache(f"user_{user_id}_caregiver_list")  # Clear user-specific caregiver list cache
    delete_from_cache(f"user_{user_id}_elderly_{assignment.elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    delete_from_cache(f"user_{user_id}_caregiver_assignments_list")  # Clear user-specific assignments list cache
    
    return new_assignment

def get_all_assignments_service(user_id: int, db: Session) -> list[CaregiverAssignmentResponse]:
    """
    Retrieve all caregiver assignments for a specific user with Redis caching.
    
    Cache Strategy:
    - Cache key: "user_{user_id}_caregiver_assignments_list"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        list[CaregiverAssignmentResponse]: List of assignments for the current user
    """
    cache_key = f"user_{user_id}_caregiver_assignments_list"

    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return [CaregiverAssignmentResponse(**a) for a in cached_data]

    # Cache miss - query database with user filter
    assignments = db.query(CaregiverAssignment).filter(CaregiverAssignment.user_id == user_id).all()
    result = [CaregiverAssignmentResponse.from_orm(a) for a in assignments]
    
    # Store result in cache for future requests
    set_in_cache(cache_key, [a.dict() for a in result], ttl=300)

    return result

def delete_assignment_service(assignment_id: int, user_id: int, db: Session) -> dict:
    """
    Delete a caregiver assignment for a specific user with Redis cache invalidation.
    
    This function clears both caregiver and elderly caches since assignments
    affect both entities' data.
    
    Args:
        assignment_id: ID of the assignment to delete
        user_id: ID of the current user (for data isolation)
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If assignment not found or doesn't belong to user
    """
    # Find and verify assignment exists and belongs to the user
    assignment = db.query(CaregiverAssignment).filter(
        CaregiverAssignment.id == assignment_id, 
        CaregiverAssignment.user_id == user_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Store IDs for cache invalidation
    caregiver_id = assignment.caregiver_id
    elderly_id = assignment.elderly_id

    # Delete from database
    db.delete(assignment)
    db.commit()

    # Invalidate related caches to ensure data consistency
    delete_from_cache(f"user_{user_id}_caregiver_{caregiver_id}")  # Clear user-specific caregiver cache
    delete_from_cache(f"user_{user_id}_caregiver_list")  # Clear user-specific caregiver list cache
    delete_from_cache(f"user_{user_id}_elderly_{elderly_id}")  # Clear user-specific elderly cache
    delete_from_cache(f"user_{user_id}_elderly_list")  # Clear user-specific elderly list cache
    delete_from_cache(f"user_{user_id}_caregiver_assignments_list")  # Clear user-specific assignments list cache

    return {"message": f"Assignment {assignment_id} deleted successfully"} 