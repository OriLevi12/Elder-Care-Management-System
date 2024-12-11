from pydantic import BaseModel, Field
from typing import Dict
from utils.pdf_generator import generate_caregiver_pdf

class Caregiver(BaseModel):
    name: str
    id: int
    bank_name: str
    bank_account: str
    branch_number: str
    salary: Dict[str, float] = Field(default={"price": 0, "amount": 0, "total": 0})
    saturday: Dict[str, float] = Field(default={"price": 0, "amount": 0, "total": 0})
    allowance: Dict[str, float] = Field(default={"price": 0, "amount": 0, "total": 0})
    total_bank: float = 0

    def update_salary(self, salary_price: float, salary_amount: int, saturday_price: float, saturday_amount: int,
                      allowance_price: float, allowance_amount: int):
        self.salary = {"price": salary_price, "amount": salary_amount, "total": salary_price * salary_amount}
        self.saturday = {"price": saturday_price, "amount": saturday_amount, "total": saturday_price * saturday_amount}
        self.allowance = {"price": allowance_price, "amount": allowance_amount, "total": allowance_price * allowance_amount}
        self.total_bank = self.salary["total"] + self.saturday["total"] + self.allowance["total"]

    def generate_pdf(self):
        return generate_caregiver_pdf(self)
