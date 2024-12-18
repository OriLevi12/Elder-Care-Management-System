from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="pending")
    elderly_id = Column(Integer, ForeignKey("elderly.id"))
    elderly = relationship("Elderly", back_populates="tasks")
