from pydantic import BaseModel, Field, ConfigDict
from typing import Dict,List
from schemas.caregiver_assignment import CaregiverAssignmentResponse

class CaregiverCreate(BaseModel):
    name: str
    custom_id: int  # User-specified ID (can be same across users)
    bank_name: str
    bank_account: str
    branch_number: str
    # user_id is automatically added by backend from logged-in user


class CaregiverUpdateSalary(BaseModel):
    salary_price: float
    salary_amount: int
    saturday_price: float
    saturday_amount: int
    allowance_price: float
    allowance_amount: int


class CaregiverResponse(BaseModel):
    id: int
    custom_id: int  # User-specified ID
    name: str
    bank_name: str
    bank_account: str
    branch_number: str
    user_id: int  # Links to user who owns this data
    salary: Dict[str, float]
    saturday: Dict[str, float]
    allowance: Dict[str, float]
    total_bank: float
    assignments: List[CaregiverAssignmentResponse] = []

    model_config = ConfigDict(from_attributes=True)
