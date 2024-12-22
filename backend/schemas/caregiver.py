from pydantic import BaseModel, Field
from typing import Dict

class CaregiverCreate(BaseModel):
    name: str
    id: int
    bank_name: str
    bank_account: str
    branch_number: str

class CaregiverUpdateSalary(BaseModel):
    salary_price: float
    salary_amount: int
    saturday_price: float
    saturday_amount: int
    allowance_price: float
    allowance_amount: int

class CaregiverResponse(BaseModel):
    id: int
    name: str
    bank_name: str
    bank_account: str
    branch_number: str
    salary: Dict[str, float]
    saturday: Dict[str, float]
    allowance: Dict[str, float]
    total_bank: float

    class Config:
        orm_mode = True
