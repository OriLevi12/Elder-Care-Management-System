from typing import List

class Elderly:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        self.tasks: List[dict] = []

    def add_task(self, task: str):
        self.tasks.append({"task": task, "status": "pending"})
