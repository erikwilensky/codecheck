from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import Base, engine
from .api import github_router, students_router, submissions_router, analyses_router, quizzes_router, upload_router, admin_router
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Code Assessment System",
    description="An intelligent system for assessing student coding assignments and detecting authentic learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
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
        "services": "running"
    }

@app.get("/status")
async def status():
    """Simple status endpoint for monitoring"""
    return {
        "status": "online",
        "service": "AI Code Assessment System",
        "version": "1.0.0"
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