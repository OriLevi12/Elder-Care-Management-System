from typing import List, Dict

class Elderly:
    elderly_list: Dict[int, "Elderly"] = {}

    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        self.tasks: List[Dict[str, str]] = []

    @classmethod
    def add(cls, name: str, id: int):
        if id in cls.elderly_list:
            raise ValueError("Elderly person already exists")
        cls.elderly_list[id] = cls(name, id)
        return cls.elderly_list[id]

    @classmethod
    def get_all(cls):
        return list(cls.elderly_list.values())

    @classmethod
    def get(cls, id: int):
        if id not in cls.elderly_list:
            raise ValueError("Elderly person not found")
        return cls.elderly_list[id]

    @classmethod
    def delete(cls, id: int):
        if id not in cls.elderly_list:
            raise ValueError("Elderly person not found")
        return cls.elderly_list.pop(id)

    def add_task(self, task: str):
        if any(t["task"] == task for t in self.tasks):
            raise ValueError(f"Task '{task}' already exists")
        self.tasks.append({"task": task, "status": "pending"})

    def delete_task(self, task: str):
        for t in self.tasks:
            if t["task"] == task:
                self.tasks.remove(t)
                return
        raise ValueError(f"Task '{task}' not found")

    def update_task_status(self, task: str, status: str):
        valid_statuses = {"pending", "in progress", "completed"}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Valid statuses are: {valid_statuses}")

        for t in self.tasks:
            if t["task"] == task:
                t["status"] = status
                return
        raise ValueError(f"Task '{task}' not found")
