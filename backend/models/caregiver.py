from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from db.database import Base

class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    bank_account = Column(String, nullable=False)
    branch_number = Column(String, nullable=False)
    salary = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})
    saturday = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})
    allowance = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})
    total_bank = Column(Float, default=0.0)
