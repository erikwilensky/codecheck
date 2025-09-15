from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    analysis_type = Column(String)  # 'basic', 'tool_detection', 'learning_progression'
    status = Column(String, default="pending")  # pending, completed, failed
    results = Column(JSON)  # Analysis results
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    student = relationship("Student", back_populates="analyses")
    submission = relationship("Submission", back_populates="analyses") 