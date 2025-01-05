from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    elderly_id = Column(Integer, ForeignKey("elderly.id", ondelete="CASCADE"), nullable=False)
    elderly = relationship("Elderly", back_populates="medications")

