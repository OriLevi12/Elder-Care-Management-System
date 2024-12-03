from typing import List

class Caregiver:
    def __init__(self, name: str, id: int, bank_name: str, bank_account: str):
        self.name = name
        self.id = id
        self.bank_name = bank_name
        self.bank_account = bank_account
        self.salary = {"price": 0, "amount": 0, "total": 0}
        self.saturday = {"price": 0, "amount": 0, "total": 0}
        self.allowance = {"price": 0, "amount": 0, "total": 0}
        self.total_bank = 0
        self.tasks: List[dict] = []

    def add_task(self, task: str):
        self.tasks.append({"task": task, "status": "pending"})
