#!/usr/bin/env python3
"""
Debug script to test AI analysis service
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_analysis_service import AIAnalysisService
from app.models import Submission
from datetime import datetime

def test_ai_service():
    """Test the AI analysis service"""
    
    # Create a test submission
    test_code = '''
def calculator():
    """Simple calculator function"""
    print("Simple Calculator")
    print("1. Add")
    print("2. Subtract") 
    print("3. Multiply")
    print("4. Divide")
    
    choice = input("Enter choice (1-4): ")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    
    if choice == '1':
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif choice == '2':
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
    elif choice == '3':
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
    elif choice == '4':
        if num2 == 0:
            print("Error: Cannot divide by zero!")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    calculator()
'''
    
    # Create test submission object
    submission = Submission(
        student_id=1,
        assignment_name="Python Calculator",
        file_name="test_calculator.py",
        file_content=test_code,
        file_size=len(test_code.encode('utf-8')),
        created_at=datetime.utcnow()
    )
    
    print("=== AI SERVICE DEBUG TEST ===")
    print("Testing AI analysis service...")
    
    try:
        # Test the AI service
        ai_service = AIAnalysisService()
        
        # Test fallback questions (this should work without API key)
        print("\nTesting fallback questions...")
        fallback_questions = ai_service._fallback_questions_with_history(submission, [])
        
        print(f"Generated {len(fallback_questions)} fallback questions")
        for i, question in enumerate(fallback_questions, 1):
            print(f"Question {i}: {question['question_text'][:50]}...")
        
        print("\n✅ Fallback questions working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_service() 