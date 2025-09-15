#!/usr/bin/env python3
"""
Simple test script for AI Code Assessment System
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from app.models import Student, Submission, Analysis, Quiz
        from app.database import get_db
        from app.main import app
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

def main():
    """Run tests"""
    print("🧪 AI Code Assessment System - Quick Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name} PASS")
            else:
                print(f"❌ {test_name} FAIL")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 System is ready!")
        print("\n📋 To start the server:")
        print("   python start.py")
        print("\n📋 Or use uvicorn directly:")
        print("   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 