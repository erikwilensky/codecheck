from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..models import get_db, Student, Submission, Assignment
from ..services.ai_analysis_service import AIAnalysisService
from datetime import datetime
import os

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/code")
async def upload_code(
    student_id: str = Form(...),
    assignment_name: str = Form(...),
    file: Optional[UploadFile] = File(None),
    code_paste: Optional[str] = Form(None),
    submission_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload code file for a student"""
    
    try:
        # Validate student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Check if assignment exists and is active
        assignment = db.query(Assignment).filter(
            Assignment.name == assignment_name,
            Assignment.is_active == True
        ).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found or inactive")
        
        # Handle file upload or code paste
        if file and file.filename:
            # File upload
            content = await file.read()
            file_content = content.decode('utf-8')
            file_name = file.filename
            file_size = len(content)
        elif code_paste:
            # Code paste
            file_content = code_paste
            file_name = f"pasted_code_{student_id}_{assignment_name}.txt"
            file_size = len(code_paste.encode('utf-8'))
        else:
            raise HTTPException(status_code=400, detail="Either file or code_paste must be provided")
        
        # Check if student already has a submission for this assignment
        existing_submission = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.assignment_name == assignment_name
        ).first()
        
        if existing_submission:
            # Delete the old submission
            print(f"Deleting old submission for student {student_id} on assignment {assignment_name}")
            db.delete(existing_submission)
            db.commit()
        
        # Create new submission
        submission = Submission(
            student_id=student.id,
            assignment_id=assignment.id,
            assignment_name=assignment_name,
            file_name=file_name,
            file_content=file_content,
            file_size=file_size,
            created_at=datetime.utcnow()
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        return {
            "success": True,
            "message": "Code uploaded successfully!",
            "submission_id": submission.id,
            "student_id": student_id,
            "assignment_name": assignment_name,
            "file_name": file_name,
            "file_size": file_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

@router.get("/submissions/{student_id}")
async def get_student_submissions(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get all submissions for a student"""
    
    submissions = db.query(Submission).filter(
        Submission.student_id == student_id
    ).order_by(Submission.created_at.desc()).all()
    
    return {
        "student_id": student_id,
        "submissions": [
            {
                "id": sub.id,
                "assignment_name": sub.assignment_name,
                "file_name": sub.file_name,
                "file_size": sub.file_size,
                "created_at": sub.created_at.isoformat()
            }
            for sub in submissions
        ]
    }

@router.get("/students")
async def get_all_students(db: Session = Depends(get_db)):
    """Get all students with direct uploads"""
    
    students = db.query(Student).all()
    
    return {
        "students": [
            {
                "id": student.id,
                "student_id": student.student_id,
                "name": student.name,
                "is_approved": student.is_approved,
                "created_at": student.created_at.isoformat()
            }
            for student in students
        ]
    } 

@router.get("/assignments")
async def get_active_assignments(db: Session = Depends(get_db)):
    """Get all active assignments for student upload page"""
    assignments = db.query(Assignment).filter(Assignment.is_active == True).order_by(Assignment.name).all()
    return {
        "assignments": [
            {
                "name": assignment.name,
                "description": assignment.description,
                "instructions": assignment.instructions
            }
            for assignment in assignments
        ]
    } 