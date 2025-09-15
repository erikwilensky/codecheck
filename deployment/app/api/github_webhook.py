from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import get_db
from ..services.github_service import GitHubService
from ..services.ai_analysis_service import AIAnalysisService
from typing import Dict, Any
import json

router = APIRouter(prefix="/webhook", tags=["GitHub Webhook"])

@router.post("/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle GitHub webhook events"""
    
    # Get request body and headers
    body = await request.body()
    headers = request.headers
    
    # Initialize services
    github_service = GitHubService()
    ai_analysis_service = AIAnalysisService()
    
    # Verify webhook signature
    signature = headers.get("x-hub-signature-256", "")
    if not github_service.verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse webhook payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Handle different event types
    event_type = headers.get("x-github-event", "")
    
    if event_type == "push":
        # Process push event
        result = github_service.process_push_event(payload, db)
        
        if result['success']:
            # Generate AI analysis and quiz for each processed commit
            for commit_result in result['results']:
                submission_id = commit_result['submission_id']
                
                # Get the submission
                from ..models import Submission
                submission = db.query(Submission).filter(Submission.id == submission_id).first()
                
                if submission:
                    # Generate AI analysis
                    analysis = ai_analysis_service.analyze_submission_with_ai(submission, db)
                    
                    # Generate AI-powered quiz
                    quiz = ai_analysis_service.generate_ai_quiz(submission, analysis, db)
            
            return {
                "status": "success",
                "message": f"Processed {result['processed_commits']} commits",
                "results": result['results']
            }
        else:
            raise HTTPException(status_code=500, detail=f"Processing failed: {result['error']}")
    
    elif event_type == "ping":
        # GitHub sends ping events to verify webhook
        return {"status": "success", "message": "Webhook verified"}
    
    else:
        # Unsupported event type
        return {"status": "ignored", "message": f"Event type '{event_type}' not supported"} 