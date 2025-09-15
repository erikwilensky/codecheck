#!/usr/bin/env python3
"""
Start script for AI Code Assessment System
"""

import os
import sys
from pathlib import Path

def main():
    """Start the server"""
    print("🚀 Starting AI Code Assessment System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: 'app' directory not found!")
        print("Make sure you're in the project root directory.")
        sys.exit(1)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("📝 Creating .env file from template...")
        if Path("env.example").exists():
            with open("env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("✅ .env file created. Please update with your API keys.")
        else:
            print("⚠️ No env.example found. Creating basic .env...")
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=your-api-key-here\n")
    
    print("✅ Environment ready")
    print("🌐 Starting server on http://127.0.0.1:8000")
    print("📝 Upload page: http://127.0.0.1:8000/upload")
    print("📚 API docs: http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 