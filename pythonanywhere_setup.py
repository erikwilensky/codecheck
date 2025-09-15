#!/usr/bin/env python3
"""
PythonAnywhere Setup Script for AI Code Assessment System
"""

import os
import sys
import sqlite3
from pathlib import Path

def create_database():
    """Create the SQLite database and tables"""
    try:
        from app.models import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✅ Database created successfully")
    except Exception as e:
        print(f"❌ Error creating database: {e}")

def create_static_directory():
    """Create static directory if it doesn't exist"""
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("✅ Static directory created")

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY', 'ADMIN_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your PythonAnywhere web app configuration")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI Code Assessment System for PythonAnywhere...")
    
    # Create static directory
    create_static_directory()
    
    # Create database
    create_database()
    
    # Check environment
    env_ok = check_environment()
    
    if env_ok:
        print("\n✅ Setup complete! Your application should be ready to run.")
        print("📝 Next steps:")
        print("1. Configure your environment variables in PythonAnywhere")
        print("2. Reload your web app")
        print("3. Visit https://codecheck.website to test your application")
    else:
        print("\n⚠️  Setup completed with warnings. Please configure missing environment variables.")

if __name__ == "__main__":
    main() 