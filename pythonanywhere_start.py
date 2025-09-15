#!/usr/bin/env python3
"""
PythonAnywhere Startup Script for AI Code Assessment System
This script initializes the application for PythonAnywhere deployment
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up environment for PythonAnywhere"""
    # Set the project path
    project_path = Path(__file__).parent.absolute()
    
    # Add to Python path
    if str(project_path) not in sys.path:
        sys.path.insert(0, str(project_path))
    
    # Change to project directory
    os.chdir(project_path)
    
    # Set environment variables with defaults
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')
    os.environ.setdefault('ADMIN_PASSWORD', 'admin123')  # Change this!
    
    print(f"✅ Project path: {project_path}")
    print(f"✅ Working directory: {os.getcwd()}")
    print(f"✅ Python path includes: {project_path}")

def initialize_database():
    """Initialize the database if it doesn't exist"""
    try:
        from app.models import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'openai', 
        'pydantic', 'python_dotenv', 'fpdf2'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        print("Please install requirements: pip install -r requirements-pythonanywhere.txt")
        return False
    else:
        print("✅ All required modules are available")
        return True

def main():
    """Main startup function"""
    print("🚀 Starting AI Code Assessment System for PythonAnywhere...")
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        return False
    
    # Initialize database
    db_ok = initialize_database()
    if not db_ok:
        return False
    
    print("\n✅ Application is ready!")
    print("📝 Next steps:")
    print("1. Set your OPENAI_API_KEY in PythonAnywhere environment variables")
    print("2. Set a secure ADMIN_PASSWORD")
    print("3. Reload your web app")
    print("4. Visit your domain to test the application")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
