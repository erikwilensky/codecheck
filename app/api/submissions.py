from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db, Submission, Student
from typing import List, Dict, Any
from fastapi.responses import Response

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("/")
async def get_submissions(
    db: Session = Depends(get_db),
    student_id: int = None,
    limit: int = 50
):
    """Get all submissions or submissions for a specific student"""
    query = db.query(Submission)
    
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    
    submissions = query.order_by(Submission.created_at.desc()).limit(limit).all()
    
    return {
        "submissions": [
            {
                "id": sub.id,
                "student_id": sub.student_id,
                "commit_sha": sub.commit_sha,
                "commit_message": sub.commit_message,
                "commit_date": sub.commit_date.isoformat() if sub.commit_date else None,
                "lines_added": sub.lines_added,
                "lines_deleted": sub.lines_deleted,
                "files_changed": sub.files_changed,
                "github_repo": sub.github_repo,
                "branch": sub.branch,
                "assignment_id": sub.assignment_id,
                "created_at": sub.created_at.isoformat() if sub.created_at else None
            }
            for sub in submissions
        ]
    }

@router.get("/{submission_id}")
async def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Get specific submission details"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Get student info
    student = db.query(Student).filter(Student.id == submission.student_id).first()
    
    return {
        "submission": {
            "id": submission.id,
            "student_id": submission.student_id,
            "student_name": student.name if student else "Unknown",
            "commit_sha": submission.commit_sha,
            "commit_message": submission.commit_message,
            "commit_date": submission.commit_date.isoformat() if submission.commit_date else None,
            "lines_added": submission.lines_added,
            "lines_deleted": submission.lines_deleted,
            "files_changed": submission.files_changed,
            "github_repo": submission.github_repo,
            "branch": submission.branch,
            "assignment_id": submission.assignment_id,
            "diff_content": submission.diff_content,
            "created_at": submission.created_at.isoformat() if submission.created_at else None
        }
    } 

@router.get("/{submission_id}/download")
async def download_submission_file(submission_id: int, db: Session = Depends(get_db)):
    """Download the file content of a submission as a text file"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    file_content = submission.file_content or ''
    file_name = getattr(submission, 'file_name', None) or 'submission.txt'
    return Response(
        content=file_content,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={file_name}"
        }
    ) 