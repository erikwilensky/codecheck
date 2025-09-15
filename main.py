#!/usr/bin/env python3
"""
Main entry point for the AI Code Assessment System
Railway-optimized version
"""

import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Get port from Railway environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Railway uses 0.0.0.0 to bind to all interfaces
    host = "0.0.0.0"
    
    # Disable reload in production (Railway)
    reload = os.environ.get("RAILWAY_ENVIRONMENT") != "production"
    
    print(f"🚀 Starting AI Code Assessment System...")
    print(f"🌐 Host: {host}")
    print(f"🌐 Port: {port}")
    print(f"🔄 Reload: {reload}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    ) 