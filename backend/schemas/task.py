from pydantic import BaseModel, Field

class TaskSchema(BaseModel):
    id: int
    description: str
    status: str = Field(default="pending")

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    description: str
    status: str = "pending"
