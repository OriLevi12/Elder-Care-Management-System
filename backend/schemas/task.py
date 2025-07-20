from pydantic import BaseModel, Field, ConfigDict

class TaskSchema(BaseModel):
    id: int
    description: str
    status: str = Field(default="pending")

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    description: str
    status: str = "pending"

   