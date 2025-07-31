from pydantic import BaseModel, ConfigDict

class CaregiverAssignmentCreate(BaseModel):
    caregiver_id: int
    elderly_id: int
    # user_id is automatically added by backend from logged-in user

class CaregiverAssignmentResponse(BaseModel):
    id: int
    caregiver_id: int
    elderly_id: int
    user_id: int  # Links to user who owns this data

    model_config = ConfigDict(from_attributes=True)