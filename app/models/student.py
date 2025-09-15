from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)  # e.g., "STU001", "STU002"
    name = Column(String)  # Student's actual name (for admin reference)
    is_approved = Column(Boolean, default=False)  # Only approved students can submit
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    block = Column(Integer, nullable=False)  # 4 or 6 only
    
    # Relationships
    submissions = relationship("Submission", back_populates="student")
    analyses = relationship("Analysis", back_populates="student")
    quizzes = relationship("Quiz", back_populates="student") 