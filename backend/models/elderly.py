from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Elderly(Base):
    """
    Elderly model representing elderly individuals in the care system.
    Each elderly person belongs to a specific user (family/care facility).
    """
    __tablename__ = "elderly"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Auto-incrementing primary key
    custom_id = Column(Integer, nullable=False)  # User-specified ID (can be same across users)
    name = Column(String, nullable=False)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to user who owns this data
    tasks = relationship("Task", back_populates="elderly", cascade="all, delete")
    medications = relationship("Medication", back_populates="elderly", cascade="all, delete")
    assignments = relationship("CaregiverAssignment", back_populates="elderly", cascade="all, delete") 
