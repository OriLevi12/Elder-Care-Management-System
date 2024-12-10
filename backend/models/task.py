from pydantic import BaseModel, Field

class Task(BaseModel):
    description: str
    status: str = Field(default="pending", pattern="^(pending|in progress|completed)$")

    def update_status(self, new_status: str):
        valid_statuses = {"pending", "in progress", "completed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status '{new_status}'. Valid statuses are: {valid_statuses}")
        self.status = new_status
