from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from db.database import get_db
from services.auth_service import login_user, create_user, get_current_user
from models.user import User
from schemas.auth import RegisterRequest, LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    Args:
        register_data: RegisterRequest containing email, password, and full_name
        db: Database session
        
    Returns:
        UserResponse: The created user information
        
    Raises:
        HTTPException: If user already exists
    """
    return create_user(email=register_data.email, password=register_data.password, full_name=register_data.full_name, db=db)

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Args:
        login_data: LoginRequest containing email and password
        db: Database session
        
    Returns:
        LoginResponse: Contains access token and user information
        
    Raises:
        HTTPException: If authentication fails
    """
    return login_user(login_data=login_data, db=db)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information from JWT token.
    
    Args:
        current_user: Current user (extracted from JWT token)
        
    Returns:
        UserResponse: Current user information
    """
    return current_user
