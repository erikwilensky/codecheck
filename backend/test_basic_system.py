#!/usr/bin/env python3
"""
Basic system test - no OpenAI API required
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

def test_student_creation():
    """Test creating a student record"""
    print("\n👤 Testing student creation...")
    
    try:
        from app.database import get_db
        from app.models import Student
        from sqlalchemy.orm import Session
        
        # Get database session
        db = next(get_db())
        
        # Create test student
        student = Student(
            student_id="CS101001",
            class_code="CS101",
            is_active=True
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        
        print(f"✅ Created student: {student.student_id}")
        
        # Clean up
        db.delete(student)
        db.commit()
        
        return True
    except Exception as e:
        print(f"❌ Student creation error: {e}")
        return False

def test_upload_api():
    """Test upload API structure"""
    print("\n📝 Testing upload API...")
    
    try:
        from app.api.upload import router
        print("✅ Upload API imported successfully")
        
        # Check if endpoints exist
        routes = [route.path for route in router.routes]
        expected_routes = ['/api/upload/code', '/api/upload/submissions/{student_id}', '/api/upload/students']
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route found: {route}")
            else:
                print(f"⚠️ Route not found: {route}")
        
        return True
    except Exception as e:
        print(f"❌ Upload API error: {e}")
        return False

def test_web_interface():
    """Test web interface files"""
    print("\n🌐 Testing web interface...")
    
    try:
        # Check if upload.html exists
        if os.path.exists("static/upload.html"):
            print("✅ Upload interface exists")
            
            # Check file size
            size = os.path.getsize("static/upload.html")
            print(f"✅ Upload interface size: {size} bytes")
            
            return True
        else:
            print("❌ Upload interface missing")
            return False
    except Exception as e:
        print(f"❌ Web interface error: {e}")
        return False

def test_server_startup():
    """Test server startup (without running)"""
    print("\n🚀 Testing server startup...")
    
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        
        # Check if routes are registered
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes")
        
        return True
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Code Assessment System - Basic Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Student Creation", test_student_creation),
        ("Upload API", test_upload_api),
        ("Web Interface", test_web_interface),
        ("Server Startup", test_server_startup)
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
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📋 Next steps:")
        print("1. Add OpenAI API key to .env file (optional)")
        print("2. Run: python start_server.py")
        print("3. Visit: http://localhost:8001/upload")
        print("4. Test with: python generate_student_ids.py")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 