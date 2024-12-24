from pydantic import BaseModel,constr

class MedicationCreate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True) 
    dosage: constr(min_length=1, strip_whitespace=True) 
    frequency: constr(min_length=1, strip_whitespace=True) 

class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str

    class Config:
        orm_mode = True
