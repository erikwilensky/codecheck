#!/usr/bin/env python3
"""
Deployment script for AI Code Assessment System
Helps prepare files for PythonAnywhere deployment
"""

import os
import shutil
import subprocess
from pathlib import Path

def create_deployment_package():
    """Create a clean deployment package"""
    
    # Create deployment directory
    deploy_dir = Path("deployment")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy essential directories
    dirs_to_copy = ["app", "static"]
    for dir_name in dirs_to_copy:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"✓ Copied {dir_name}/")
    
    # Copy essential files
    files_to_copy = [
        "requirements.txt",
        "init_db.py",
        "wsgi.py",
        "env.example"
    ]
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, deploy_dir / file_name)
            print(f"✓ Copied {file_name}")
    
    # Create .env template
    env_template = """# AI Code Assessment System Environment Variables
# Replace these values with your actual configuration

OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./ai_assessment.db
ADMIN_PASSWORD=your_secure_admin_password

# Optional: Customize these settings
DEBUG=False
HOST=0.0.0.0
PORT=8000
"""
    
    with open(deploy_dir / ".env", "w") as f:
        f.write(env_template)
    print("✓ Created .env template")
    
    # Create deployment instructions
    instructions = """# PythonAnywhere Deployment Instructions

## Directory Structure:
Your AI Code Assessment System will be deployed to:
/home/yourusername/ai-assessment-system/

This keeps it separate from your other webapp in /home/yourusername/oyco-data/

## Quick Setup:

1. Upload all files in this directory to: /home/yourusername/ai-assessment-system/
2. Create virtual environment: mkvirtualenv ai-assessment
3. Install requirements: pip install -r requirements.txt
4. Set up your .env file with real values
5. Initialize database: python init_db.py
6. Configure WSGI file with your username
7. Set up static files in PythonAnywhere web app
8. Add your custom domain
9. Reload web app

## Files included:
- app/ - Main application code
- static/ - HTML/CSS/JS files
- requirements.txt - Python dependencies
- init_db.py - Database initialization
- wsgi.py - WSGI configuration
- .env - Environment variables template

## PythonAnywhere Setup Steps:

1. **Create new web app:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.9 or 3.10

2. **Upload files:**
   - Go to "Files" tab
   - Navigate to /home/yourusername/
   - Create directory: ai-assessment-system
   - Upload all files from this deployment package

3. **Configure WSGI:**
   - Edit the WSGI file in PythonAnywhere
   - Replace 'yourusername' with your actual username
   - Add your API keys and passwords

4. **Set up static files:**
   - URL: /static/
   - Directory: /home/yourusername/ai-assessment-system/static/

5. **Add your domain** to the web app

## Next steps:
1. Replace 'yourusername' in wsgi.py with your PythonAnywhere username
2. Add your OpenAI API key to .env
3. Set a secure admin password
4. Configure your domain in PythonAnywhere
"""
    
    with open(deploy_dir / "DEPLOYMENT_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    print("✓ Created deployment instructions")
    
    print(f"\n🎉 Deployment package created in: {deploy_dir}")
    print("Upload this directory to: /home/yourusername/ai-assessment-system/")
    print("This keeps it separate from your oyco-data webapp!")

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "app/main.py",
        "static/admin.html", 
        "static/upload.html",
        "requirements.txt",
        "init_db.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✓ All required files found")
    return True

def main():
    print("🚀 AI Code Assessment System - Deployment Package Creator")
    print("=" * 60)
    
    if not check_requirements():
        print("\n❌ Please ensure all required files exist before creating deployment package")
        return
    
    create_deployment_package()
    
    print("\n📋 Next Steps:")
    print("1. Go to PythonAnywhere.com and create an account")
    print("2. Create directory: /home/yourusername/ai-assessment-system/")
    print("3. Upload the 'deployment' folder contents to that directory")
    print("4. Follow the DEPLOYMENT_INSTRUCTIONS.txt file")
    print("5. Set up your custom domain from Namecheap")
    print("\n📚 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 