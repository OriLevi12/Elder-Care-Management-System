from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from db.database import Base
from sqlalchemy.orm import relationship
import os

# Use JSONB for PostgreSQL, JSON for SQLite
if os.getenv("TESTING"):
    JSONType = SQLiteJSON
else:
    JSONType = JSONB

class Caregiver(Base):
    """
    Caregiver model representing professional caregivers in the care system.
    Each caregiver belongs to a specific user (family/care facility).
    """
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Auto-incrementing primary key
    custom_id = Column(Integer, nullable=False)  # User-specified ID (can be same across users)
    name = Column(String, nullable=False)  # Name of the caregiver
    bank_name = Column(String, nullable=False)  # Bank name for payments
    bank_account = Column(String, nullable=False)  # Bank account number
    branch_number = Column(String, nullable=False)  # Bank branch number
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to user who owns this data
    salary = Column(JSONType, default={"price": 0, "amount": 0, "total": 0})  # Salary information
    saturday = Column(JSONType, default={"price": 0, "amount": 0, "total": 0})  # Saturday work information
    allowance = Column(JSONType, default={"price": 0, "amount": 0, "total": 0})  # Allowance information
    total_bank = Column(Float, default=0.0)  # Total bank amount
    assignments = relationship("CaregiverAssignment", back_populates="caregiver", cascade="all, delete")
