from typing import Dict
from utils.pdf_generator import generate_caregiver_pdf

class Caregiver:
    caregivers: Dict[int, "Caregiver"] = {}

    def __init__(self, name: str, id: int, bank_name: str, bank_account: str, branch_number: str):
        self.name = name
        self.id = id
        self.bank_name = bank_name
        self.bank_account = bank_account
        self.branch_number = branch_number
        self.salary = {"price": 0, "amount": 0, "total": 0}
        self.saturday = {"price": 0, "amount": 0, "total": 0}
        self.allowance = {"price": 0, "amount": 0, "total": 0}
        self.total_bank = 0

    @classmethod
    def add(cls, name: str, id: int, bank_name: str, bank_account: str, branch_number: str):
        if id in cls.caregivers:
            raise ValueError("Caregiver already exists")
        cls.caregivers[id] = cls(name, id, bank_name, bank_account, branch_number)
        return cls.caregivers[id]

    @classmethod
    def get_all(cls):
        return list(cls.caregivers.values())

    @classmethod
    def get(cls, id: int):
        if id not in cls.caregivers:
            raise ValueError("Caregiver not found")
        return cls.caregivers[id]

    @classmethod
    def delete(cls, id: int):
        if id not in cls.caregivers:
            raise ValueError("Caregiver not found")
        return cls.caregivers.pop(id)

    def update_salary(self, salary_price: float, salary_amount: int, saturday_price: float, saturday_amount: int,
                      allowance_price: float, allowance_amount: int):
        self.salary = {"price": salary_price, "amount": salary_amount, "total": salary_price * salary_amount}
        self.saturday = {"price": saturday_price, "amount": saturday_amount, "total": saturday_price * saturday_amount}
        self.allowance = {"price": allowance_price, "amount": allowance_amount, "total": allowance_price * allowance_amount}
        self.total_bank = self.salary["total"] + self.saturday["total"] + self.allowance["total"]

    def generate_pdf(self):
        return generate_caregiver_pdf(self)
