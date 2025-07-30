from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Elderly(Base):
    """
    Elderly model representing elderly individuals in the care system.
    Each elderly person belongs to a specific user (family/care facility).
    """
    __tablename__ = "elderly"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)  # Name of the elderly person
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to user who owns this data
    tasks = relationship("Task", back_populates="elderly", cascade="all, delete")
    medications = relationship("Medication", back_populates="elderly", cascade="all, delete")
    assignments = relationship("CaregiverAssignment", back_populates="elderly", cascade="all, delete") 
