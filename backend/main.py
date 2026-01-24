from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
# Allow origins from environment variable or default to localhost for development
# In production, set ALLOWED_ORIGINS to include your frontend URL (e.g., "https://your-app.vercel.app")
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# If ALLOWED_ORIGINS is "*", allow all origins (but can't use credentials)
if "*" in allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(caregivers.router, prefix="/caregivers", tags=["caregivers"])
app.include_router(elderly.router, prefix="/elderly", tags=["elderly"])
app.include_router(caregiver_assignments.router, prefix="/caregiver-assignments", tags=["caregiver-assignments"])
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Elder Care Management System!"}