#!/usr/bin/env python3
"""
PythonAnywhere ASGI startup script
Simple version that should work
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to project directory
os.chdir(project_root)

# Set environment variables (use defaults, override with actual values in production)
os.environ.setdefault('OPENAI_API_KEY', 'your_openai_api_key_here')
os.environ.setdefault('ADMIN_PASSWORD', 'quizscope!')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')

# Import the app
from app.main import app

# Export the app for uvicorn to use
# No need to run uvicorn here - PythonAnywhere handles that