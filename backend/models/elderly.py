from pydantic import BaseModel
from typing import List
from models.task import Task

class Elderly(BaseModel):
    id: int
    name: str
    tasks: List[Task] = []

    def add_task(self, task: Task):
        if any(t.description == task.description for t in self.tasks):
            raise ValueError(f"Task '{task.description}' already exists")
        self.tasks.append(task)

    def delete_task(self, description: str):
        for task in self.tasks:
            if task.description == description:
                self.tasks.remove(task)
                return
        raise ValueError(f"Task '{description}' not found")

    def update_task_status(self, description: str, new_status: str):
        for task in self.tasks:
            if task.description == description:
                task.update_status(new_status)
                return task
        raise ValueError(f"Task '{description}' not found")
