#!/usr/bin/env python3
"""
Test AI Analysis with Historical Context
Demonstrates how the AI analyzes submissions with complete historical context
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import get_db
from app.models import Student, Submission, Analysis
from app.services.ai_analysis_service import AIAnalysisService

def create_test_data():
    """Create test data with historical submissions"""
    db = next(get_db())
    
    # Create test student
    student = Student(
        name="Test Student",
        email="test@example.com",
        github_username="teststudent",
        created_at=datetime.utcnow()
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    # Create historical submissions (simulating learning progression)
    submissions = []
    
    # Week 1: Basic understanding
    submissions.append(Submission(
        student_id=student.id,
        github_repo="teststudent/learning-project",
        commit_sha="abc123",
        commit_message="Initial commit - basic setup",
        commit_date=datetime.utcnow() - timedelta(days=21),
        files_changed=["main.py"],
        lines_added=10,
        lines_deleted=0,
        diff_content="+ print('Hello World')",
        created_at=datetime.utcnow() - timedelta(days=21)
    ))
    
    # Week 2: Simple function
    submissions.append(Submission(
        student_id=student.id,
        github_repo="teststudent/learning-project",
        commit_sha="def456",
        commit_message="Add simple function",
        commit_date=datetime.utcnow() - timedelta(days=14),
        files_changed=["main.py"],
        lines_added=15,
        lines_deleted=2,
        diff_content="+ def greet(name):\n+     return f'Hello {name}'",
        created_at=datetime.utcnow() - timedelta(days=14)
    ))
    
    # Week 3: Basic error handling
    submissions.append(Submission(
        student_id=student.id,
        github_repo="teststudent/learning-project",
        commit_sha="ghi789",
        commit_message="Add error handling",
        commit_date=datetime.utcnow() - timedelta(days=7),
        files_changed=["main.py"],
        lines_added=25,
        lines_deleted=5,
        diff_content="+ try:\n+     result = process_data()\n+ except Exception as e:\n+     print(f'Error: {e}')",
        created_at=datetime.utcnow() - timedelta(days=7)
    ))
    
    # Current submission: Advanced features (potential tool usage)
    current_submission = Submission(
        student_id=student.id,
        github_repo="teststudent/learning-project",
        commit_sha="jkl012",
        commit_message="Implement comprehensive data validation and error handling with advanced logging capabilities",
        commit_date=datetime.utcnow(),
        files_changed=["main.py", "utils.py", "config.py"],
        lines_added=150,
        lines_deleted=10,
        diff_content="+ import logging\n+ from typing import Optional, Dict, Any\n+ def validate_data(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:\n+     logger = logging.getLogger(__name__)\n+     try:\n+         validated = process_complex_data(data)\n+         logger.info('Data validation successful')\n+         return validated\n+     except ValidationError as e:\n+         logger.error(f'Validation failed: {e}')\n+         return None",
        created_at=datetime.utcnow()
    )
    
    # Add all submissions to database
    for submission in submissions:
        db.add(submission)
    db.add(current_submission)
    db.commit()
    
    return student, current_submission, db

def test_ai_analysis_with_history():
    """Test AI analysis with historical context"""
    print("🤖 Testing AI Analysis with Historical Context")
    print("=" * 60)
    
    try:
        # Create test data
        student, current_submission, db = create_test_data()
        
        print(f"✅ Created test student: {student.name}")
        print(f"✅ Created {len(db.query(Submission).filter(Submission.student_id == student.id).all())} historical submissions")
        print(f"✅ Current submission: {current_submission.commit_message[:50]}...")
        
        # Initialize AI analysis service
        ai_service = AIAnalysisService()
        
        print("\n🔍 Running AI analysis with historical context...")
        
        # Perform AI analysis
        analysis = ai_service.analyze_submission_with_ai(current_submission, db)
        
        print(f"✅ Analysis completed: {analysis.analysis_type}")
        print(f"✅ Confidence score: {analysis.confidence_score}")
        
        # Display analysis results
        results = analysis.results
        print("\n📊 AI Analysis Results:")
        print("-" * 40)
        
        # Historical Analysis
        historical = results.get('historical_analysis', {})
        print(f"📈 Learning Trajectory: {historical.get('learning_trajectory', 'unknown')}")
        print(f"📈 Consistency Score: {historical.get('consistency_score', 0.0):.2f}")
        print(f"📈 Improvement Rate: {historical.get('improvement_rate', 0.0):.2f}")
        
        # Tool Dependency
        tool_dep = results.get('tool_dependency', {})
        print(f"\n🔍 Tool Dependency Analysis:")
        print(f"   AI Usage Probability: {tool_dep.get('ai_usage_probability', 0.0):.2f}")
        print(f"   Copilot Usage Probability: {tool_dep.get('copilot_usage_probability', 0.0):.2f}")
        print(f"   Copy-Paste Probability: {tool_dep.get('copy_paste_probability', 0.0):.2f}")
        print(f"   Confidence: {tool_dep.get('confidence', 0.0):.2f}")
        
        # Learning Progression
        learning = results.get('learning_progression', {})
        print(f"\n🎓 Learning Progression:")
        print(f"   Overall Progression: {learning.get('overall_progression', 'unknown')}")
        print(f"   Understanding Level: {learning.get('understanding_level', 'unknown')}")
        print(f"   Skill Development Rate: {learning.get('skill_development_rate', 0.0):.2f}")
        
        # Authentic Learning Assessment
        authentic = results.get('authentic_learning_assessment', {})
        print(f"\n✅ Authentic Learning Assessment:")
        print(f"   Authentic Learning Score: {authentic.get('authentic_learning_score', 0.0):.2f}")
        print(f"   Genuine Understanding: {authentic.get('genuine_understanding', True)}")
        print(f"   Gradual Improvement: {authentic.get('gradual_improvement', True)}")
        print(f"   Consistent Approach: {authentic.get('consistent_approach', True)}")
        
        # Intervention Recommendations
        intervention = results.get('intervention_recommendations', {})
        print(f"\n🚨 Intervention Recommendations:")
        print(f"   Intervention Needed: {intervention.get('intervention_needed', False)}")
        print(f"   Intervention Type: {intervention.get('intervention_type', 'none')}")
        print(f"   Priority: {intervention.get('priority', 'low')}")
        
        # Generate AI quiz
        print("\n📝 Generating AI-powered quiz...")
        quiz = ai_service.generate_ai_quiz(current_submission, analysis, db)
        
        print(f"✅ Quiz generated: {quiz.quiz_type}")
        print(f"✅ Total questions: {quiz.total_questions}")
        
        # Display quiz questions
        questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz.id).all()
        print(f"\n📋 Quiz Questions:")
        for i, question in enumerate(questions, 1):
            print(f"\n   Question {i}: {question.question_type}")
            print(f"   Text: {question.question_text[:100]}...")
            print(f"   Difficulty: {question.difficulty}")
            print(f"   Learning Objectives: {question.learning_objectives}")
        
        print("\n🎉 AI Analysis with Historical Context Test Completed Successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during AI analysis test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_analysis():
    """Test fallback analysis when OpenAI is not available"""
    print("\n🔄 Testing Fallback Analysis (No OpenAI)")
    print("=" * 50)
    
    try:
        # Temporarily remove OpenAI API key
        original_key = os.environ.get('OPENAI_API_KEY')
        if original_key:
            del os.environ['OPENAI_API_KEY']
        
        # Create test data
        student, current_submission, db = create_test_data()
        
        # Initialize AI analysis service
        ai_service = AIAnalysisService()
        
        print("🔍 Running fallback analysis...")
        
        # Perform analysis (should use fallback)
        analysis = ai_service.analyze_submission_with_ai(current_submission, db)
        
        print(f"✅ Fallback analysis completed: {analysis.analysis_type}")
        print(f"✅ Analysis method: {analysis.results.get('analysis_method', 'unknown')}")
        
        # Restore API key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
        
        print("✅ Fallback analysis test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during fallback test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Analysis with Historical Context Test Suite")
    print("=" * 60)
    
    # Test 1: Full AI analysis
    success1 = test_ai_analysis_with_history()
    
    # Test 2: Fallback analysis
    success2 = test_fallback_analysis()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   AI Analysis Test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"   Fallback Test: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! AI analysis with historical context is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.") 