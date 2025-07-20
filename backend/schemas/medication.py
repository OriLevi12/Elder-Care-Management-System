from pydantic import BaseModel,constr, ConfigDict

class MedicationCreate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True) 
    dosage: constr(min_length=1, strip_whitespace=True) 
    frequency: constr(min_length=1, strip_whitespace=True) 

class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str

    model_config = ConfigDict(from_attributes=True)
