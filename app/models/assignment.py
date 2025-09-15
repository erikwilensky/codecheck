from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "Python Calculator", "Data Structures"
    description = Column(Text)  # Detailed description of the assignment
    instructions = Column(Text)  # Step-by-step instructions for students
    is_active = Column(Boolean, default=True)  # Whether assignment is available for submissions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="assignment") 