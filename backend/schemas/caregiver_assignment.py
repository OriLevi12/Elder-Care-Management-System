from pydantic import BaseModel, ConfigDict

class CaregiverAssignmentCreate(BaseModel):
    caregiver_id: int
    elderly_id: int

class CaregiverAssignmentResponse(BaseModel):
    id: int
    caregiver_id: int
    elderly_id: int

    model_config = ConfigDict(from_attributes=True)