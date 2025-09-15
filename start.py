#!/usr/bin/env python3
"""
Render startup script for AI Code Assessment System
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to project directory
os.chdir(project_root)

# Set environment variables with defaults
os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')
os.environ.setdefault('ADMIN_PASSWORD', 'admin123')
os.environ.setdefault('OPENAI_API_KEY', 'your_openai_api_key_here')
os.environ.setdefault('PORT', '8000')
os.environ.setdefault('RENDER', 'true')

# Import and run the app
if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    port = int(os.environ.get("PORT", 10000))  # Render default port
    host = "0.0.0.0"
    
    print(f"🚀 Starting AI Code Assessment System on Render...")
    print(f"🌐 Host: {host}")
    print(f"🌐 Port: {port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )