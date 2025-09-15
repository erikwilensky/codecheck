#!/usr/bin/env python3
"""
Main entry point for the AI Code Assessment System
DigitalOcean-optimized version
"""

import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Get port from DigitalOcean environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # DigitalOcean uses 0.0.0.0 to bind to all interfaces
    host = "0.0.0.0"
    
    # Disable reload in production (DigitalOcean)
    reload = os.environ.get("DIGITALOCEAN_ENVIRONMENT") != "production"
    
    print(f"🚀 Starting AI Code Assessment System on DigitalOcean...")
    print(f"🌐 Host: {host}")
    print(f"🌐 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🔧 Database: {os.environ.get('DATABASE_URL', 'sqlite:///./ai_assessment.db')}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    ) 