from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class User(Base):
    """
    User model for authentication and data isolation.
    Each user represents a head of their own organization (family/care facility).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)  # Used for login
    hashed_password = Column(String, nullable=False)  # Encrypted password for security
    full_name = Column(String)  # Display name for the user
    is_active = Column(Boolean, default=True)  # Enable/disable user account
