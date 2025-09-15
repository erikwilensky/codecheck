"""
PythonAnywhere-optimized main application for AI Code Assessment System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import Base, engine
from .api import github_router, students_router, submissions_router, analyses_router, quizzes_router, upload_router, admin_router
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for PythonAnywhere
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app with PythonAnywhere-optimized settings
app = FastAPI(
    title="AI Code Assessment System",
    description="An intelligent system for assessing student coding assignments and detecting authentic learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# PythonAnywhere-specific CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://erikwilensky.pythonanywhere.com",
        "https://codecheck.website",
        "http://localhost:8000",  # For local testing
        "https://*.pythonanywhere.com"  # Allow all PythonAnywhere subdomains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(github_router)
app.include_router(students_router)
app.include_router(submissions_router)
app.include_router(analyses_router)
app.include_router(quizzes_router)
app.include_router(upload_router)
app.include_router(admin_router, prefix='/admin')

@app.get("/")
async def root():
    """Root endpoint - redirects to upload page"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/upload")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": "running",
        "platform": "pythonanywhere"
    }

@app.get("/status")
async def status():
    """Simple status endpoint for monitoring"""
    return {
        "status": "online",
        "service": "AI Code Assessment System",
        "version": "1.0.0",
        "platform": "pythonanywhere"
    }

@app.get("/docs")
async def get_docs():
    """Get API documentation"""
    return {
        "message": "API documentation available at /docs",
        "swagger_ui": "/docs",
        "redoc": "/redoc"
    }

@app.get("/upload")
async def upload_page():
    """Serve the upload page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/upload.html")

@app.get("/admin")
async def admin_page():
    """Serve the admin panel page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/admin.html")

# PythonAnywhere-specific startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("🚀 AI Code Assessment System starting on PythonAnywhere...")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔧 Database URL: {os.getenv('DATABASE_URL', 'sqlite:///./ai_assessment.db')}")
    
    # Ensure static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("✅ Created static directory")

# PythonAnywhere-specific shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 AI Code Assessment System shutting down...")
