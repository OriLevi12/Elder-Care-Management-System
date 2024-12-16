from sqlalchemy import Column, Integer, String
from db.database import Base
from pydantic import BaseModel

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency: str

class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str

    class Config:
        orm_mode = True
