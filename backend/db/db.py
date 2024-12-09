from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL for connecting to the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/db/eldercare.db"

# Create a SQLAlchemy engine to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal through which we will interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the database models
Base = declarative_base()
