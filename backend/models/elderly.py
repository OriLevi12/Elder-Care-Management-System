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

    def add_task(self, task: str):
        if task in self.tasks:
            raise ValueError(f"Task '{task}' already exists")
        self.tasks.append(task)

    def delete_task(self, task: str):
        if task not in self.tasks:
            raise ValueError(f"Task '{task}' not found")
        self.tasks.remove(task)
