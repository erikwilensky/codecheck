"""
PythonAnywhere-specific configuration for AI Code Assessment System
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
STATIC_DIR = PROJECT_ROOT / "static"
DATABASE_PATH = PROJECT_ROOT / "ai_assessment.db"

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# CORS settings for PythonAnywhere
ALLOWED_ORIGINS = [
    "https://erikwilensky.pythonanywhere.com",
    "https://codecheck.website",
    "http://localhost:8000",  # For local testing
]

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.py', '.js', '.html', '.css', '.txt', '.md'}

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# PythonAnywhere-specific settings
PYTHONANYWHERE = {
    'username': 'erikwilensky',
    'project_path': '/home/erikwilensky/code_share',
    'static_url': '/static/',
    'domain': 'codecheck.website'
}

def get_config():
    """Get configuration dictionary"""
    return {
        'database_url': DATABASE_URL,
        'openai_api_key': OPENAI_API_KEY,
        'admin_password': ADMIN_PASSWORD,
        'secret_key': SECRET_KEY,
        'allowed_origins': ALLOWED_ORIGINS,
        'max_file_size': MAX_FILE_SIZE,
        'allowed_extensions': ALLOWED_EXTENSIONS,
        'log_level': LOG_LEVEL,
        'pythonanywhere': PYTHONANYWHERE
    }

def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required")
    
    if ADMIN_PASSWORD == 'admin123':
        errors.append("Please change ADMIN_PASSWORD from default value")
    
    if SECRET_KEY == 'your-secret-key-change-this':
        errors.append("Please change SECRET_KEY from default value")
    
    return errors
