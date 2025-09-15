#!/usr/bin/env python3
"""
Test script to demonstrate improved quiz generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_analysis_service import AIAnalysisService
from app.models import Submission, Student
from app.models.database import get_db, engine
from sqlalchemy.orm import sessionmaker

def test_quiz_generation():
    """Test the improved quiz generation with fallback questions"""
    
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
        student_id=1,  # Will be replaced with actual student ID
        assignment_name="Python Calculator",
        file_name="test_calculator.py",
        file_content=test_code,
        file_size=len(test_code.encode('utf-8'))
    )
    
    # Test the fallback questions
    ai_service = AIAnalysisService()
    questions = ai_service._fallback_questions_with_history(submission, [])
    
    print("=== IMPROVED QUIZ GENERATION TEST ===")
    print(f"Generated {len(questions)} questions for: {submission.assignment_name}")
    print()
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}:")
        print(f"  Type: {question['question_type']}")
        print(f"  Text: {question['question_text']}")
        print(f"  Difficulty: {question['difficulty']}")
        print(f"  Learning Objectives: {', '.join(question['learning_objectives'])}")
        if question.get('code_snippet'):
            print(f"  Code Snippet: {question['code_snippet']}")
        print()

if __name__ == "__main__":
    test_quiz_generation() 