from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db, Student, Submission, Analysis, Quiz
from ..services.github_service import GitHubService
from typing import List, Dict, Any

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
async def get_students(db: Session = Depends(get_db), class_id: str = None):
    """Get all students or students in a specific class"""
    query = db.query(Student)
    
    if class_id:
        query = query.filter(Student.class_id == class_id)
    
    students = query.all()
    
    return {
        "students": [
            {
                "id": student.id,
                "name": student.name,
                "github_username": student.github_username,
                "email": student.email,
                "class_id": student.class_id,
                "is_active": student.is_active,
                "created_at": student.created_at.isoformat() if student.created_at else None
            }
            for student in students
        ]
    }

@router.get("/{student_id}")
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get specific student details"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get recent submissions
    recent_submissions = db.query(Submission).filter(
        Submission.student_id == student_id
    ).order_by(Submission.created_at.desc()).limit(10).all()
    
    # Get recent analyses
    recent_analyses = db.query(Analysis).filter(
        Analysis.student_id == student_id
    ).order_by(Analysis.created_at.desc()).limit(5).all()
    
    # Get recent quizzes
    recent_quizzes = db.query(Quiz).filter(
        Quiz.student_id == student_id
    ).order_by(Quiz.created_at.desc()).limit(5).all()
    
    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "github_username": student.github_username,
            "email": student.email,
            "class_id": student.class_id,
            "is_active": student.is_active,
            "created_at": student.created_at.isoformat() if student.created_at else None
        },
        "recent_submissions": [
            {
                "id": sub.id,
                "commit_sha": sub.commit_sha,
                "commit_message": sub.commit_message,
                "commit_date": sub.commit_date.isoformat() if sub.commit_date else None,
                "lines_added": sub.lines_added,
                "lines_deleted": sub.lines_deleted,
                "files_changed": len(sub.files_changed) if sub.files_changed else 0
            }
            for sub in recent_submissions
        ],
        "recent_analyses": [
            {
                "id": analysis.id,
                "analysis_type": analysis.analysis_type,
                "status": analysis.status,
                "confidence_score": analysis.confidence_score,
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None
            }
            for analysis in recent_analyses
        ],
        "recent_quizzes": [
            {
                "id": quiz.id,
                "quiz_type": quiz.quiz_type,
                "status": quiz.status,
                "total_questions": quiz.total_questions,
                "score": quiz.score,
                "created_at": quiz.created_at.isoformat() if quiz.created_at else None
            }
            for quiz in recent_quizzes
        ]
    }

@router.get("/{student_id}/submissions")
async def get_student_submissions(
    student_id: int, 
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get student submissions"""
    submissions = db.query(Submission).filter(
        Submission.student_id == student_id
    ).order_by(Submission.created_at.desc()).limit(limit).all()
    
    return {
        "submissions": [
            {
                "id": sub.id,
                "commit_sha": sub.commit_sha,
                "commit_message": sub.commit_message,
                "commit_date": sub.commit_date.isoformat() if sub.commit_date else None,
                "lines_added": sub.lines_added,
                "lines_deleted": sub.lines_deleted,
                "files_changed": sub.files_changed,
                "github_repo": sub.github_repo,
                "branch": sub.branch,
                "assignment_id": sub.assignment_id
            }
            for sub in submissions
        ]
    }

@router.get("/{student_id}/analyses")
async def get_student_analyses(
    student_id: int,
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get student analyses"""
    analyses = db.query(Analysis).filter(
        Analysis.student_id == student_id
    ).order_by(Analysis.created_at.desc()).limit(limit).all()
    
    return {
        "analyses": [
            {
                "id": analysis.id,
                "analysis_type": analysis.analysis_type,
                "status": analysis.status,
                "results": analysis.results,
                "confidence_score": analysis.confidence_score,
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
                "completed_at": analysis.completed_at.isoformat() if analysis.completed_at else None
            }
            for analysis in analyses
        ]
    }

@router.get("/{student_id}/quizzes")
async def get_student_quizzes(
    student_id: int,
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get student quizzes"""
    quizzes = db.query(Quiz).filter(
        Quiz.student_id == student_id
    ).order_by(Quiz.created_at.desc()).limit(limit).all()
    
    return {
        "quizzes": [
            {
                "id": quiz.id,
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