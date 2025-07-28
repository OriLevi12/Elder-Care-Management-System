from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.caregiver_assignment import CaregiverAssignmentCreate, CaregiverAssignmentResponse
from models.caregiver import Caregiver
from models.elderly import Elderly
from models.caregiver_assignments import CaregiverAssignment
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def create_assignment_service(assignment: CaregiverAssignmentCreate, db: Session) -> CaregiverAssignmentResponse:
    """
    Create a new caregiver assignment with Redis cache invalidation.
    
    This function clears both caregiver and elderly caches since assignments
    affect both entities' data.
    
    Args:
        assignment: CaregiverAssignmentCreate schema containing assignment data
        db: Database session
        
    Returns:
        CaregiverAssignmentResponse: The created assignment
        
    Raises:
        HTTPException: If caregiver or elderly not found, or assignment already exists
    """
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
    new_assignment = CaregiverAssignment(
        caregiver_id=assignment.caregiver_id, 
        elderly_id=assignment.elderly_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    # Invalidate related caches to ensure data consistency
    print("🧹 Clearing caregiver and elderly caches due to assignment change")
    delete_from_cache(f"caregiver_{assignment.caregiver_id}")  # Clear caregiver cache
    delete_from_cache("caregiver_list")  # Clear caregiver list cache
    delete_from_cache(f"elderly_{assignment.elderly_id}")  # Clear elderly cache
    delete_from_cache("elderly_list")  # Clear elderly list cache
    
    return new_assignment

def get_all_assignments_service(db: Session) -> list[CaregiverAssignmentResponse]:
    """
    Retrieve all caregiver assignments with Redis caching.
    
    Cache Strategy:
    - Cache key: "caregiver_assignments_list"
    - TTL: 300 seconds (5 minutes)
    - On cache hit: Return cached data
    - On cache miss: Query DB, cache result, return data
    
    Args:
        db: Database session
        
    Returns:
        list[CaregiverAssignmentResponse]: List of all assignments
    """
    cache_key = "caregiver_assignments_list"

    # Try to get data from Redis cache first
    cached_data = get_from_cache(cache_key)
    if cached_data:
        print("✅ Retrieved caregiver assignments list from Redis cache")
        return [CaregiverAssignmentResponse(**a) for a in cached_data]

    # Cache miss - query database
    assignments = db.query(CaregiverAssignment).all()
    result = [CaregiverAssignmentResponse.from_orm(a) for a in assignments]
    
    # Store result in cache for future requests
    print("📦 Retrieved caregiver assignments list from DB and storing in Redis")
    set_in_cache(cache_key, [a.dict() for a in result], ttl=300)

    return result

def delete_assignment_service(assignment_id: int, db: Session) -> dict:
    """
    Delete a caregiver assignment with Redis cache invalidation.
    
    This function clears both caregiver and elderly caches since assignments
    affect both entities' data.
    
    Args:
        assignment_id: ID of the assignment to delete
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If assignment not found
    """
    # Find and verify assignment exists
    assignment = db.query(CaregiverAssignment).filter(CaregiverAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Store IDs for cache invalidation
    caregiver_id = assignment.caregiver_id
    elderly_id = assignment.elderly_id

    # Delete from database
    db.delete(assignment)
    db.commit()

    # Invalidate related caches to ensure data consistency
    print("🧹 Clearing caregiver and elderly caches due to assignment deletion")
    delete_from_cache(f"caregiver_{caregiver_id}")  # Clear caregiver cache
    delete_from_cache("caregiver_list")  # Clear caregiver list cache
    delete_from_cache(f"elderly_{elderly_id}")  # Clear elderly cache
    delete_from_cache("elderly_list")  # Clear elderly list cache
    delete_from_cache("caregiver_assignments_list")  # Clear assignments list cache

    return {"message": f"Assignment {assignment_id} deleted successfully"} 