#!/usr/bin/env python3
"""
Test script to verify the openai_client fix works
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to project directory
os.chdir(project_root)

# Set environment variables
os.environ.setdefault('OPENAI_API_KEY', 'sk-test-key')
os.environ.setdefault('ADMIN_PASSWORD', 'quizscope!')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')

try:
    from app.services.openai_client import get_client_or_none
    
    print("Testing openai_client fix...")
    client = get_client_or_none()
    
    if client:
        print(f"✅ Client created successfully: {type(client)}")
        print(f"Client type: {client}")
    else:
        print("❌ No client created (API key not set)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
