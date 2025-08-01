from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    """Schema for user registration request"""
    email: EmailStr
    password: str
    full_name: str

class LoginRequest(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Schema for successful login response"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: str

class UserResponse(BaseModel):
    """Schema for user information in API responses"""
    id: int
    email: str
    full_name: str
    is_active: bool
