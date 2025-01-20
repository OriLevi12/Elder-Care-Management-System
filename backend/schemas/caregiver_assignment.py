from pydantic import BaseModel

class CaregiverAssignmentCreate(BaseModel):
    caregiver_id: int
    elderly_id: int

class CaregiverAssignmentResponse(BaseModel):
    id: int
    caregiver_id: int
    elderly_id: int

    class Config:
        orm_mode = True
