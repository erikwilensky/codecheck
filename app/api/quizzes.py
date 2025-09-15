from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db, Quiz, QuizQuestion, Student
from typing import List, Dict, Any

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.get("/")
async def get_quizzes(
    db: Session = Depends(get_db),
    student_id: int = None,
    quiz_type: str = None,
    limit: int = 50
):
    """Get all quizzes or quizzes for a specific student"""
    query = db.query(Quiz)
    
    if student_id:
        query = query.filter(Quiz.student_id == student_id)
    
    if quiz_type:
        query = query.filter(Quiz.quiz_type == quiz_type)
    
    quizzes = query.order_by(Quiz.created_at.desc()).limit(limit).all()
    
    return {
        "quizzes": [
            {
                "id": quiz.id,
                "student_id": quiz.student_id,
                "submission_id": quiz.submission_id,
                "quiz_type": quiz.quiz_type,
                "status": quiz.status,
                "total_questions": quiz.total_questions,
                "correct_answers": quiz.correct_answers,
                "score": quiz.score,
                "created_at": quiz.created_at.isoformat() if quiz.created_at else None,
                "completed_at": quiz.completed_at.isoformat() if quiz.completed_at else None
            }
            for quiz in quizzes
        ]
    }

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get specific quiz with questions"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get questions
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    
    # Get student info
    student = db.query(Student).filter(Student.id == quiz.student_id).first()
    
    return {
        "quiz": {
            "id": quiz.id,
            "student_id": quiz.student_id,
            "student_name": student.name if student else "Unknown",
            "submission_id": quiz.submission_id,
            "quiz_type": quiz.quiz_type,
            "status": quiz.status,
            "total_questions": quiz.total_questions,
            "correct_answers": quiz.correct_answers,
            "score": quiz.score,
            "created_at": quiz.created_at.isoformat() if quiz.created_at else None,
            "completed_at": quiz.completed_at.isoformat() if quiz.completed_at else None
        },
        "questions": [
            {
                "id": question.id,
                "question_type": question.question_type,
                "question_text": question.question_text,
                "code_snippet": question.code_snippet,
                "options": question.options,
                "correct_answer": question.correct_answer,
                "student_answer": question.student_answer,
                "is_correct": question.is_correct,
                "explanation": question.explanation,
                "difficulty": question.difficulty,
                "learning_objectives": question.learning_objectives
            }
            for question in questions
        ]
    }

@router.get("/{quiz_id}/questions")
async def get_quiz_questions(quiz_id: int, db: Session = Depends(get_db)):
    """Get questions for a specific quiz"""
    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="Quiz questions not found")
    
    return {
        "questions": [
            {
                "id": question.id,
                "question_type": question.question_type,
                "question_text": question.question_text,
                "code_snippet": question.code_snippet,
                "options": question.options,
                "correct_answer": question.correct_answer,
                "student_answer": question.student_answer,
                "is_correct": question.is_correct,
                "explanation": question.explanation,
                "difficulty": question.difficulty,
                "learning_objectives": question.learning_objectives
            }
            for question in questions
        ]
    } 