from pydantic import BaseModel

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
