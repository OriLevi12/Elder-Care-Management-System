from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class CaregiverAssignment(Base):
    __tablename__ = "caregiver_assignments"

    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    elderly_id = Column(Integer, ForeignKey("elderly.id"), nullable=False)

    caregiver = relationship("Caregiver", back_populates="assignments")
    elderly = relationship("Elderly", back_populates="assignments")
