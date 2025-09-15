#!/usr/bin/env python3
"""
Initialize database with all models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import engine, Base
from app.models import student, submission, analysis, quiz, assignment

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    # NOTE: If you add new columns (like 'block' to Student), you must re-initialize the database or use a migration tool like Alembic.

if __name__ == "__main__":
    init_database() 