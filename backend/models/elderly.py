from models.task import Task
from pydantic import BaseModel
from typing import List, Dict

elderly_list: Dict[int, "Elderly"] = {}

class Elderly(BaseModel):
    id: int
    name: str
    tasks: List[str] = []

    @classmethod
    def add(cls, name: str, id: int):
        if id in elderly_list:
            raise ValueError("Elderly person already exists")
        elderly = cls(id=id, name=name)
        elderly_list[id] = elderly
        return elderly

    @classmethod
    def get_all(cls):
        return list(elderly_list.values())

    @classmethod
    def get(cls, id: int):
        if id not in elderly_list:
            raise ValueError("Elderly person not found")
        return elderly_list[id]

    @classmethod
    def delete(cls, id: int):
        if id not in elderly_list:
            raise ValueError("Elderly person not found")
        return elderly_list.pop(id)


    def add_task(self, description: str):
        if any(t.description == description for t in self.tasks):
            raise ValueError(f"Task '{description}' already exists")
        self.tasks.append(Task(description=description))


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
