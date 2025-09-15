from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_assessment.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Create metadata
metadata = MetaData()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database with all tables"""
    from .models import student, submission, analysis, quiz, quiz_question
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

def drop_db():
    """Drop all tables (for testing)"""
    Base.metadata.drop_all(bind=engine)
    print("🗑️ Database dropped successfully!") 