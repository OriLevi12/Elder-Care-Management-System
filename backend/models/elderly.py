from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Elderly(Base):
    __tablename__ = "elderly"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="elderly", cascade="all, delete")
    medications = relationship("Medication", back_populates="elderly", cascade="all, delete") 
