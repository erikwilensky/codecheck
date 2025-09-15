from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db, Analysis, Student
from typing import List, Dict, Any

router = APIRouter(prefix="/analyses", tags=["Analyses"])

@router.get("/")
async def get_analyses(
    db: Session = Depends(get_db),
    student_id: int = None,
    analysis_type: str = None,
    limit: int = 50
):
    """Get all analyses or analyses for a specific student"""
    query = db.query(Analysis)
    
    if student_id:
        query = query.filter(Analysis.student_id == student_id)
    
    if analysis_type:
        query = query.filter(Analysis.analysis_type == analysis_type)
    
    analyses = query.order_by(Analysis.created_at.desc()).limit(limit).all()
    
    return {
        "analyses": [
            {
                "id": analysis.id,
                "student_id": analysis.student_id,
                "submission_id": analysis.submission_id,
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

@router.get("/{analysis_id}")
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Get specific analysis details"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Get student info
    student = db.query(Student).filter(Student.id == analysis.student_id).first()
    
    return {
        "analysis": {
            "id": analysis.id,
            "student_id": analysis.student_id,
            "student_name": student.name if student else "Unknown",
            "submission_id": analysis.submission_id,
            "analysis_type": analysis.analysis_type,
            "status": analysis.status,
            "results": analysis.results,
            "confidence_score": analysis.confidence_score,
            "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
            "completed_at": analysis.completed_at.isoformat() if analysis.completed_at else None
        }
    } 