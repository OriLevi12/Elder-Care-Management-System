from pydantic import BaseModel
from typing import List
from schemas.task import TaskSchema
from schemas.medication import MedicationResponse
from schemas.caregiver_assignment import CaregiverAssignmentResponse

class ElderlySchema(BaseModel):
    id: int
    name: str
    tasks: List[TaskSchema] = []
    medications: List[MedicationResponse] = []
    assignments: List[CaregiverAssignmentResponse] = []
    
    class Config:
        orm_mode = True

class ElderlyCreate(BaseModel):
    id: int  
    name: str
