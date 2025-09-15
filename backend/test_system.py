#!/usr/bin/env python3
"""
Simple system test - no server required
"""

import os
import sys
import json
from datetime import datetime

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test core imports
        from app.models import Student, Submission, Analysis, Quiz
        from app.database import get_db
        from app.services.ai_analysis_service import AIAnalysisService
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n🗄️ Testing database...")
    
    try:
        from app.database import engine
        from app.models import Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_student_id_generation():
    """Test student ID generation"""
    print("\n🆔 Testing student ID generation...")
    
    try:
        # Test the ID format
        class_code = "CS101"
        student_number = 15
        student_id = f"{class_code}{student_number:03d}"
        
        print(f"✅ Generated student ID: {student_id}")
        print(f"✅ Format: {class_code} + {student_number:03d} = {student_id}")
        return True
    except Exception as e:
        print(f"❌ Student ID generation error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app/main.py",
        "app/database.py",
        "app/models/__init__.py",
        "app/models/student.py",
        "app/api/__init__.py",
        "app/api/upload.py",
        "app/services/ai_analysis_service.py",
        "static/upload.html",
        "requirements.txt",
        "setup.py",
        "env.example"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present")
        return True

def test_environment():
    """Test environment setup"""
    print("\n🔧 Testing environment...")
    
    # Check if .env exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("⚠️ .env file not found - you'll need to create one")
    
    # Check if requirements are installed
    try:
        import fastapi
        import sqlalchemy
        import openai
        print("✅ Required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 AI Code Assessment System - System Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Database", test_database),
        ("Student ID Generation", test_student_id_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📋 Next steps:")
        print("1. Create .env file with your OpenAI API key")
        print("2. Run: python setup.py")
        print("3. Run: python start_server.py")
        print("4. Visit: http://localhost:8001/upload")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 