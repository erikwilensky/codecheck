#!/usr/bin/env python3
"""
Simple server startup script
"""

import uvicorn
import os
import sys

def main():
    """Start the server on a different port"""
    
    # Add the current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Starting AI Code Assessment System...")
    print("📝 Upload page will be available at: http://localhost:8001/upload")
    print("🔍 API docs will be available at: http://localhost:8001/docs")
    print("📊 Health check at: http://localhost:8001/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start server on port 8001 to avoid conflicts
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 