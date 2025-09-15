from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from typing import List
from ..models import get_db, Student, Submission, Analysis, Quiz, QuizQuestion, QuizPDF, Assignment
from datetime import datetime
import csv
import io
from pydantic import BaseModel
from ..services.quiz_generation_service import QuizGenerationService
from ..services.quiz_service import create_quiz_pdf, store_quiz_pdf_in_db
from ..services.ai_analysis_service import AIAnalysisService

class QuizGenerationRequest(BaseModel):
    assignment_name: str
    student_ids: List[str]

class AssignmentCreateRequest(BaseModel):
    name: str
    description: str
    instructions: str

class AssignmentUpdateRequest(BaseModel):
    name: str
    description: str
    instructions: str
    is_active: bool

# Simple password protection dependency
ADMIN_PASSWORD = 'quizscope!'

def require_admin_password(request: Request):
    password = request.headers.get('X-Admin-Password') or request.query_params.get('password')
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail='Unauthorized: Invalid admin password')

router = APIRouter(tags=["Admin"], dependencies=[Depends(require_admin_password)])

@router.post("/upload-students")
async def upload_students_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Received file: {file if file else 'None'}; filename: {getattr(file, 'filename', None)}")
    """
    Upload CSV file with student names and IDs
    CSV format: name,student_id
    """
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        students_processed = 0
        students_updated = 0
        students_created = 0
        
        for row in csv_reader:
            if 'name' not in row or 'student_id' not in row or 'block' not in row:
                raise HTTPException(status_code=400, detail="CSV must have 'name', 'student_id', and 'block' columns")
            
            name = row['name'].strip()
            student_id = row['student_id'].strip()
            block = row['block'].strip()
            
            if not name or not student_id or not block:
                continue
            
            if block not in ('4', '6'):
                raise HTTPException(status_code=400, detail="Block must be 4 or 6")
            block = int(block)
            
            # Check if student already exists
            existing_student = db.query(Student).filter(Student.student_id == student_id).first()
            
            if existing_student:
                # Update existing student
                existing_student.name = name
                existing_student.block = block
                existing_student.is_approved = True
                existing_student.updated_at = datetime.utcnow()
                students_updated += 1
            else:
                # Create new student
                student = Student(
                    student_id=student_id,
                    name=name,
                    block=block,
                    is_approved=True,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.add(student)
                students_created += 1
            
            students_processed += 1
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Student list updated successfully",
            "students_processed": students_processed,
            "students_created": students_created,
            "students_updated": students_updated
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV processing failed: {str(e)}")

@router.get("/students")
async def get_all_students(db: Session = Depends(get_db), block: int = None):
    """Get all students (admin view)"""
    query = db.query(Student)
    if block in (4, 6):
        query = query.filter(Student.block == block)
    students = query.order_by(Student.name).all()
    return {
        "students": [
            {
                "id": student.id,
                "student_id": student.student_id,
                "name": student.name,
                "block": student.block,
                "is_approved": student.is_approved,
                "created_at": student.created_at.isoformat(),
                "submission_count": len(student.submissions),
                "latest_assignment": student.submissions[-1].assignment_name if student.submissions else None,
                "submissions": [
                    {
                        "id": sub.id,
                        "assignment_name": sub.assignment_name,
                        "file_name": sub.file_name,
                        "created_at": sub.created_at.isoformat()
                    }
                    for sub in student.submissions
                ]
            }
            for student in students
        ]
    }

@router.get("/students/{student_id}")
async def get_student(student_id: str, db: Session = Depends(get_db)):
    """Get a specific student by student_id"""
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "student": {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "is_approved": student.is_approved,
            "created_at": student.created_at.isoformat(),
            "updated_at": student.updated_at.isoformat() if student.updated_at else None,
            "submission_count": len(student.submissions),
            "latest_assignment": student.submissions[-1].assignment_name if student.submissions else None,
            "submissions": [
                {
                    "id": sub.id,
                    "assignment_name": sub.assignment_name,
                    "file_name": sub.file_name,
                    "file_size": sub.file_size,
                    "created_at": sub.created_at.isoformat()
                }
                for sub in student.submissions
            ]
        }
    }

@router.put("/students/{student_id}")
async def update_student(
    student_id: str,
    request: dict, # Expects JSON body with fields to update
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    name = request.get('name')
    block = request.get('block')
    if block not in ('4', '6', 4, 6):
        raise HTTPException(status_code=400, detail="Block must be 4 or 6")
    student.name = name
    student.block = int(block)
    student.is_approved = request.get('is_approved', student.is_approved)
    student.updated_at = datetime.utcnow()
    db.commit()
    return {"success": True, "message": "Student updated successfully"}

@router.post("/students/{student_id}/approve")
async def approve_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Approve a student for submissions"""
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.is_approved = True
    student.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "message": f"Student {student_id} approved for submissions"
    }

@router.post("/students/{student_id}/disapprove")
async def disapprove_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Disapprove a student (prevent submissions)"""
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.is_approved = False
    student.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "message": f"Student {student_id} disapproved (cannot submit)"
    }

@router.delete("/students/{student_id}")
async def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Delete a student (admin only)"""
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    
    return {
        "success": True,
        "message": f"Student {student_id} deleted"
    }

@router.post("/generate-quiz")
async def generate_quiz(
    request: QuizGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate quizzes for selected students using AI analysis"""
    
    # Generate quiz questions using AI
    try:
        # Get all submissions for the selected students and assignment
        submissions = []
        print(f"Debug: Looking for submissions for students {request.student_ids} and assignment '{request.assignment_name}'")
        
        for student_id in request.student_ids:
            # Find student by string student_id
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if student:
                print(f"Debug: Found student {student.name} (DB ID: {student.id})")
                # Get submissions for this student and assignment
                student_submissions = db.query(Submission).filter(
                    Submission.student_id == student.id,  # Use database ID
                    Submission.assignment_name == request.assignment_name
                ).all()
                print(f"Debug: Found {len(student_submissions)} submissions for student {student.name}")
                submissions.extend(student_submissions)
            else:
                print(f"Debug: Student with ID {student_id} not found")
        
        print(f"Debug: Total submissions found: {len(submissions)}")
        
        if not submissions:
            raise HTTPException(status_code=400, detail="No submissions found for selected students and assignment")
        
        # Get student names
        student_names = []
        for student_id in request.student_ids:
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if student:
                student_names.append(student.name)
        
        # Combine all code content for analysis
        all_code_content = "\n\n".join([sub.file_content for sub in submissions])
        
        # Generate questions using the new quiz service
        print(f"Debug: About to call quiz generation service with content length: {len(all_code_content)}")
        quiz_service = QuizGenerationService()
        try:
            questions = await quiz_service.generate_quiz_questions(all_code_content, request.assignment_name)
            print(f"Debug: Received {len(questions)} questions")
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=f"Quiz generation service unavailable: {str(e)}")
        
        # Create quiz data from QuizQuestion objects
        quiz_data = []
        for i, q in enumerate(questions, 1):
            quiz_data.append({
                "question_text": q.question,
                "code_snippet": q.code_snippet,
                "focus": q.focus,
                "question_number": i
            })
        
        print(f"Debug: Created quiz_data: {quiz_data}")
        
        # Create separate PDF data for each student
        pdf_quiz_data = []
        for i, student_id in enumerate(request.student_ids):
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if student:
                pdf_quiz_data.append({
                    "name": student.name,
                    "student_id": student_id,
                    "questions": quiz_data
                })
        
        # Generate PDF
        pdf_info = create_quiz_pdf(pdf_quiz_data, request.assignment_name)
        
        # Store PDF in database
        quiz_pdf = store_quiz_pdf_in_db(pdf_info, db)
        
        return {
            "success": True,
            "message": f"Quiz generated successfully! PDF ID: {quiz_pdf.id}",
            "pdf_id": quiz_pdf.id,
            "questions_count": len(quiz_data)
        }
        
    except Exception as e:
        print(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@router.get("/quiz-pdfs")
async def list_quiz_pdfs(db: Session = Depends(get_db)):
    """List all generated quiz PDFs"""
    
    pdfs = db.query(QuizPDF).order_by(QuizPDF.created_at.desc()).all()
    
    return {
        "pdfs": [
            {
                "id": pdf.id,
                "assignment_name": pdf.assignment_name,
                "pdf_filename": pdf.pdf_filename,
                "student_count": pdf.student_count,
                "student_ids": pdf.student_ids,
                "created_at": pdf.created_at.isoformat(),
                "generated_by": pdf.generated_by
            }
            for pdf in pdfs
        ]
    }

@router.get("/quiz-pdfs/{pdf_id}/download")
async def download_quiz_pdf(pdf_id: int, db: Session = Depends(get_db)):
    """Download a specific quiz PDF"""
    
    quiz_pdf = db.query(QuizPDF).filter(QuizPDF.id == pdf_id).first()
    if not quiz_pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return Response(
        content=quiz_pdf.pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={quiz_pdf.pdf_filename}"
        }
    )

@router.delete("/quiz-pdfs/{pdf_id}")
async def delete_quiz_pdf(pdf_id: int, db: Session = Depends(get_db)):
    """Delete a quiz PDF"""
    
    quiz_pdf = db.query(QuizPDF).filter(QuizPDF.id == pdf_id).first()
    if not quiz_pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    db.delete(quiz_pdf)
    db.commit()
    
    return {
        "success": True,
        "message": f"PDF {quiz_pdf.pdf_filename} deleted successfully"
    }

@router.delete("/quiz-pdfs/delete-all")
async def delete_all_quiz_pdfs(db: Session = Depends(get_db)):
    """Delete all quiz PDFs"""
    count = db.query(QuizPDF).delete()
    db.commit()
    return {"success": True, "message": f"Deleted {count} quiz PDFs."}

# Assignment Management Endpoints

@router.get("/assignments")
async def get_all_assignments(db: Session = Depends(get_db)):
    """Get all assignments"""
    
    assignments = db.query(Assignment).order_by(Assignment.name).all()
    
    return {
        "assignments": [
            {
                "id": assignment.id,
                "name": assignment.name,
                "description": assignment.description,
                "instructions": assignment.instructions,
                "is_active": assignment.is_active,
                "created_at": assignment.created_at.isoformat(),
                "updated_at": assignment.updated_at.isoformat(),
                "submission_count": len(assignment.submissions)
            }
            for assignment in assignments
        ]
    }

@router.post("/assignments")
async def create_assignment(
    request: AssignmentCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new assignment"""
    
    # Check if assignment name already exists
    existing = db.query(Assignment).filter(Assignment.name == request.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Assignment with this name already exists")
    
    assignment = Assignment(
        name=request.name,
        description=request.description,
        instructions=request.instructions,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    
    return {
        "success": True,
        "message": f"Assignment '{request.name}' created successfully",
        "assignment": {
            "id": assignment.id,
            "name": assignment.name,
            "description": assignment.description,
            "instructions": assignment.instructions,
            "is_active": assignment.is_active
        }
    }

@router.get("/assignments/{assignment_id}")
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific assignment"""
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {
        "assignment": {
            "id": assignment.id,
            "name": assignment.name,
            "description": assignment.description,
            "instructions": assignment.instructions,
            "is_active": assignment.is_active,
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
            "submission_count": len(assignment.submissions)
        }
    }

@router.put("/assignments/{assignment_id}")
async def update_assignment(
    assignment_id: int,
    request: AssignmentUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update an assignment"""
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if new name conflicts with existing assignment
    if request.name != assignment.name:
        existing = db.query(Assignment).filter(Assignment.name == request.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Assignment with this name already exists")
    
    assignment.name = request.name
    assignment.description = request.description
    assignment.instructions = request.instructions
    assignment.is_active = request.is_active
    assignment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assignment)
    
    return {
        "success": True,
        "message": f"Assignment '{request.name}' updated successfully",
        "assignment": {
            "id": assignment.id,
            "name": assignment.name,
            "description": assignment.description,
            "instructions": assignment.instructions,
            "is_active": assignment.is_active
        }
    }

@router.patch("/assignments/{assignment_id}/toggle")
async def toggle_assignment_status(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """Toggle assignment active status"""
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    assignment.is_active = not assignment.is_active
    assignment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assignment)
    
    status = "activated" if assignment.is_active else "deactivated"
    
    return {
        "success": True,
        "message": f"Assignment '{assignment.name}' {status} successfully",
        "assignment": {
            "id": assignment.id,
            "name": assignment.name,
            "is_active": assignment.is_active
        }
    }

@router.delete("/assignments/{assignment_id}")
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    """Delete an assignment"""
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if assignment has submissions
    if len(assignment.submissions) > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete assignment '{assignment.name}' - it has {len(assignment.submissions)} submissions"
        )
    
    db.delete(assignment)
    db.commit()
    
    return {
        "success": True,
        "message": f"Assignment '{assignment.name}' deleted successfully"
    } 