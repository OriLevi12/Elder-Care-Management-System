from fastapi import FastAPI
from db.database import Base, engine
from routes import caregivers, elderly, caregiver_assignments, auth
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Elder Care Management System",
    description="A system for managing caregivers, medications, tasks, and daily operations for elderly individuals.",
    version="1.0.0"
)

app.include_router(caregivers.router, prefix="/caregivers", tags=["caregivers"])
app.include_router(elderly.router, prefix="/elderly", tags=["elderly"])
app.include_router(caregiver_assignments.router, prefix="/caregiver-assignments", tags=["caregiver-assignments"])
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Elder Care Management System!"}

