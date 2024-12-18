from pydantic import BaseModel
from typing import List
from schemas.task import TaskSchema

class ElderlySchema(BaseModel):
    id: int
    name: str
    tasks: List[TaskSchema] = []

    class Config:
        orm_mode = True

class ElderlyCreate(BaseModel):
    id: int  
    name: str
