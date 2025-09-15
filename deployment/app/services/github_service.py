import os
import hmac
import hashlib
from typing import Dict, Any, Optional
from github import Github
from github.Repository import Repository
from github.Commit import Commit
from sqlalchemy.orm import Session
from ..models import Student, Submission
from datetime import datetime
import json

class GitHubService:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET")
        self.github = Github(self.github_token) if self.github_token else None
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify GitHub webhook signature"""
        if not self.webhook_secret:
            return True  # Skip verification if no secret configured
        
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def process_push_event(self, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Process GitHub push event and store commit data"""
        try:
            # Extract commit information
            commits = payload.get('commits', [])
            repository = payload.get('repository', {})
            ref = payload.get('ref', '')
            
            results = []
            
            for commit_data in commits:
                # Find or create student
                student = self._get_or_create_student(commit_data, db)
                
                # Create submission record
                submission = self._create_submission(
                    student, commit_data, repository, ref, db
                )
                
                results.append({
                    'student_id': student.id,
                    'submission_id': submission.id,
                    'commit_sha': commit_data['id'],
                    'status': 'processed'
                })
            
            return {
                'success': True,
                'processed_commits': len(results),
                'results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_or_create_student(self, commit_data: Dict[str, Any], db: Session) -> Student:
        """Get or create student based on commit author"""
        author = commit_data.get('author', {})
        github_username = author.get('username', 'unknown')
        email = author.get('email', '')
        name = author.get('name', github_username)
        
        # Try to find existing student
        student = db.query(Student).filter(
            Student.github_username == github_username
        ).first()
        
        if not student:
            # Create new student
            student = Student(
                github_username=github_username,
                email=email,
                name=name,
                class_id='default'  # Will be updated when teacher assigns
            )
            db.add(student)
            db.commit()
            db.refresh(student)
        
        return student
    
    def _create_submission(self, student: Student, commit_data: Dict[str, Any], 
                          repository: Dict[str, Any], ref: str, db: Session) -> Submission:
        """Create submission record from commit data"""
        
        # Calculate basic metrics
        files_changed = []
        lines_added = 0
        lines_deleted = 0
        
        for file_change in commit_data.get('modified', []):
            files_changed.append(file_change)
        
        for file_change in commit_data.get('added', []):
            files_changed.append(file_change)
        
        # Create submission
        submission = Submission(
            student_id=student.id,
            github_repo=repository.get('full_name', ''),
            commit_sha=commit_data['id'],
            commit_message=commit_data.get('message', ''),
            commit_date=datetime.fromisoformat(commit_data['timestamp'].replace('Z', '+00:00')),
            files_changed=files_changed,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
            diff_content=commit_data.get('url', ''),  # We'll fetch actual diff later
            branch=ref.replace('refs/heads/', ''),
            assignment_id='default'  # Will be updated when teacher assigns
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        return submission
    
    def get_student_submissions(self, student_id: int, db: Session, 
                              limit: int = 50) -> list:
        """Get recent submissions for a student"""
        submissions = db.query(Submission).filter(
            Submission.student_id == student_id
        ).order_by(Submission.created_at.desc()).limit(limit).all()
        
        return submissions
    
    def get_class_submissions(self, class_id: str, db: Session, 
                            limit: int = 100) -> list:
        """Get recent submissions for a class"""
        submissions = db.query(Submission).join(Student).filter(
            Student.class_id == class_id
        ).order_by(Submission.created_at.desc()).limit(limit).all()
        
        return submissions 