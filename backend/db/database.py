from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use SQLite for tests, PostgreSQL for production
if os.getenv("TESTING"):
    DATABASE_URL = "sqlite:///./test.db"
    print(f"🔍 Using SQLite database: {DATABASE_URL}")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is required for production")
    print(f"🔍 Using PostgreSQL database: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
