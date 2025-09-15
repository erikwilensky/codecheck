from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))  # New foreign key
    assignment_name = Column(String, index=True)  # Keep for backward compatibility
    file_name = Column(String)  # Original file name
    file_content = Column(Text)  # File content
    file_size = Column(Integer)  # File size in bytes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    analyses = relationship("Analysis", back_populates="submission") 