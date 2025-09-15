from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import QuizPDF
from datetime import datetime
from fpdf import FPDF
    
def create_quiz_pdf(quiz_data: List[Dict[str, Any]], assignment_name: str) -> Dict[str, Any]:
    """Create a condensed PDF file with quizzes for multiple students and return data"""
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    # Remove the initial title page
    # pdf.add_page()
    # (Title page code removed)
    
    # Generate quiz for each student
    for student in quiz_data:
        # Start new page for each student
        pdf.add_page()
        
        # Student header - compact
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Student: {student['name']} ({student['student_id']})", ln=True)
        pdf.cell(0, 6, txt=f"Assignment: {assignment_name}", ln=True)
        pdf.ln(5)
        
        # Questions - much more condensed
        pdf.set_font("Arial", '', 10)
        for i, question in enumerate(student['questions'], 1):
            # Question number and text
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(15, 6, txt=f"{i}. ", ln=False)
            
            pdf.set_font("Arial", '', 10)
            question_text = question['question_text']
            
            # Handle long questions by wrapping text properly
            if len(question_text) > 60:
                words = question_text.split()
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) <= 60:
                        current_line += " " + word if current_line else word
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                
                # Print first line on same line as question number
                if lines:
                    pdf.cell(0, 6, txt=lines[0], ln=True)
                    # Print remaining lines with proper indentation
                    for line in lines[1:]:
                        pdf.cell(15, 6, txt="", ln=False)  # Indent
                        pdf.cell(0, 6, txt=line.strip(), ln=True)
            else:
                pdf.cell(0, 6, txt=question_text, ln=True)
            
            # Add code snippet if available - very compact
            if question.get('code_snippet'):
                pdf.ln(2)
                pdf.set_font("Arial", 'I', 8)
                pdf.cell(15, 4, txt="", ln=False)  # Indent
                pdf.cell(0, 4, txt="Code:", ln=True)
                pdf.set_font("Courier", '', 7)
                code_lines = question['code_snippet'].split('\n')
                for line in code_lines[:3]:  # Limit to first 3 lines
                    pdf.cell(15, 4, txt="", ln=False)  # Indent
                    pdf.cell(0, 4, txt=line, ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.ln(2)
            
            # Add options if they exist - compact format
            if question.get('options') and len(question['options']) > 0:
                pdf.ln(2)
                for j, option in enumerate(question['options'], 1):
                    pdf.cell(15, 4, txt="", ln=False)  # Indent
                    pdf.cell(0, 4, txt=f"{j}. {option}", ln=True)
            
            pdf.ln(3)
        # Removed the 'Answers:' label and answer space
    
    # Get PDF data as bytes
    pdf_bytes = pdf.output(dest='S')
    
    # Generate filename for reference
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"quizzes_{assignment_name.replace(' ', '_')}_{timestamp}.pdf"
    
    return {
        "pdf_data": pdf_bytes,
        "pdf_filename": pdf_filename,
        "student_count": len(quiz_data),
        "assignment_name": assignment_name,
        "quiz_data": quiz_data
    }

def store_quiz_pdf_in_db(pdf_info: Dict[str, Any], db: Session) -> QuizPDF:
    """Store generated PDF in the database"""
    
    # Extract student IDs from quiz data
    student_ids = [student['student_id'] for student in pdf_info['quiz_data']]
    
    # Create QuizPDF record
    quiz_pdf = QuizPDF(
        assignment_name=pdf_info['assignment_name'],
        pdf_filename=pdf_info['pdf_filename'],
        pdf_data=pdf_info['pdf_data'],
        student_count=pdf_info['student_count'],
        student_ids=student_ids,
        quiz_data=pdf_info['quiz_data'],
        created_at=datetime.utcnow()
    )
    
    db.add(quiz_pdf)
    db.commit()
    db.refresh(quiz_pdf)
        
    return quiz_pdf 