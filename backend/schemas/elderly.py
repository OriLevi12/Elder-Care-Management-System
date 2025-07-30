from pydantic import BaseModel, ConfigDict
from typing import List
from schemas.task import TaskSchema
from schemas.medication import MedicationResponse
from schemas.caregiver_assignment import CaregiverAssignmentResponse

class ElderlySchema(BaseModel):
    id: int
    name: str
    user_id: int  # Links to user who owns this data
    tasks: List[TaskSchema] = []
    medications: List[MedicationResponse] = []
    assignments: List[CaregiverAssignmentResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ElderlyCreate(BaseModel):
    id: int  
    name: str
    # user_id is automatically added by backend from logged-in user
