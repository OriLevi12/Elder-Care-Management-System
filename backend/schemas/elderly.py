from pydantic import BaseModel
from typing import List
from schemas.task import TaskSchema
from schemas.medication import MedicationResponse

class ElderlySchema(BaseModel):
    id: int
    name: str
    tasks: List[TaskSchema] = []
    medications: List[MedicationResponse] = []
    class Config:
        orm_mode = True

class ElderlyCreate(BaseModel):
    id: int  
    name: str
