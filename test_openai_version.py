#!/usr/bin/env python3
"""
Test script to check OpenAI version and client creation
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
os.environ.setdefault('OPENAI_API_KEY', 'your_openai_api_key_here')
os.environ.setdefault('ADMIN_PASSWORD', 'quizscope!')
os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')

try:
    import openai
    print(f"OpenAI version: {openai.__version__}")
    print(f"OpenAI module: {openai}")
    
    # Test the old API format
    openai.api_key = "test-key"
    print("Old API format works")
    
    # Test the new API format
    from openai import OpenAI
    client = OpenAI(api_key="test-key")
    print("New API format works")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

