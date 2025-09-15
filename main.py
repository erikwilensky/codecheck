#!/usr/bin/env python3
"""
Main entry point for the AI Code Assessment System
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    ) 