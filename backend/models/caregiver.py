from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from db.database import Base
from sqlalchemy.orm import relationship

class Caregiver(Base):
    """
    Caregiver model representing professional caregivers in the care system.
    Each caregiver belongs to a specific user (family/care facility).
    """
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Name of the caregiver
    bank_name = Column(String, nullable=False)  # Bank name for payments
    bank_account = Column(String, nullable=False)  # Bank account number
    branch_number = Column(String, nullable=False)  # Bank branch number
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to user who owns this data
    salary = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})  # Salary information
    saturday = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})  # Saturday work information
    allowance = Column(JSONB, default={"price": 0, "amount": 0, "total": 0})  # Allowance information
    total_bank = Column(Float, default=0.0)  # Total bank amount
    assignments = relationship("CaregiverAssignment", back_populates="caregiver", cascade="all, delete")
