from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    quiz_type = Column(String)  # 'differential', 'understanding', 'debugging'
    status = Column(String, default="generated")  # generated, completed, expired
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    student = relationship("Student", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_type = Column(String)  # 'multiple_choice', 'code_explanation', 'debugging'
    question_text = Column(Text)
    code_snippet = Column(Text)
    options = Column(JSON)  # For multiple choice questions
    correct_answer = Column(String)
    student_answer = Column(String)
    is_correct = Column(Boolean)
    explanation = Column(Text)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    learning_objectives = Column(JSON)  # List of learning objectives
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")

class QuizPDF(Base):
    __tablename__ = "quiz_pdfs"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_name = Column(String, index=True)
    pdf_filename = Column(String)  # Original filename for reference
    pdf_data = Column(LargeBinary)  # Actual PDF file data
    student_count = Column(Integer)  # Number of students in this PDF
    generated_by = Column(String, default="admin")  # Who generated it
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata for easy querying
    student_ids = Column(JSON)  # List of student IDs included
    quiz_data = Column(JSON)  # Store the quiz data used to generate PDF 