#!/usr/bin/env python3
"""
Setup script for AI Code Assessment System
Initializes the database and validates the environment
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'openai',
        'requests',
        'python-multipart'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ All dependencies are installed")

def check_environment():
    """Check environment variables"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print("✅ Environment variables are set")
    return True

def init_database():
    """Initialize the database"""
    try:
        # Import directly from app
        from app.database import engine
        from app.models import Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(__file__).parent / '.env'
    env_example = Path(__file__).parent / 'env.example'
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created. Please update with your API keys.")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 AI Code Assessment System Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    check_dependencies()
    
    # Create .env file if needed
    env_ok = create_env_file()
    
    # Check environment variables
    env_vars_ok = check_environment()
    
    # Initialize database
    db_ok = init_database()
    
    print("\n" + "=" * 40)
    print("📊 Setup Summary:")
    print(f"   Python Version: ✅")
    print(f"   Dependencies: ✅")
    print(f"   Environment: {'✅' if env_vars_ok else '⚠️'}")
    print(f"   Database: {'✅' if db_ok else '❌'}")
    
    if env_vars_ok and db_ok:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update your .env file with API keys")
        print("2. Run: python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8080")
        print("3. Test with: python test_ai_analysis_with_history.py")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("Please address the issues above before running the system.")

if __name__ == "__main__":
    main() 