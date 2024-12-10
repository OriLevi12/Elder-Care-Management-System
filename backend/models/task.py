from pydantic import BaseModel, Field

class Task(BaseModel):
    description: str
    status: str = Field(default="pending", pattern="^(pending|in progress|completed)$")
