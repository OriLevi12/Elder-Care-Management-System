from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class CaregiverAssignment(Base):
    """
    CaregiverAssignment model representing assignments between caregivers and elderly.
    Each assignment belongs to a specific user (family/care facility).
    """
    __tablename__ = "caregiver_assignments"

    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)  # Links to caregiver
    elderly_id = Column(Integer, ForeignKey("elderly.id"), nullable=False)  # Links to elderly
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to user who owns this data

    caregiver = relationship("Caregiver", back_populates="assignments")
    elderly = relationship("Elderly", back_populates="assignments")
