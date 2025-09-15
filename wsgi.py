import sys
import os
from pathlib import Path

# Add your project directory to Python path
# Update this path to match your PythonAnywhere username and project location
project_path = '/home/erikwilensky/code_share'
if project_path not in sys.path:
    sys.path.append(project_path)

# Set working directory
os.chdir(project_path)

# Set environment variables
# These will be configured in PythonAnywhere's web app settings
os.environ.setdefault('OPENAI_API_KEY', 'your_openai_api_key_here')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')
os.environ.setdefault('ADMIN_PASSWORD', 'your_secure_admin_password')

# Import your FastAPI app (PythonAnywhere-optimized version)
from app.main_pythonanywhere import app

# For WSGI - PythonAnywhere expects 'application'
application = app 