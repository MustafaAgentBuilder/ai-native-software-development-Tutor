# Claude is Work to Build this Project
"""
TutorGPT Platform - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from tutor_agent.api.v1 import content, auth
from tutor_agent.config.settings import get_settings
from tutor_agent.core.database import init_db

# Initialize settings
settings = get_settings()

# CRITICAL: Set OpenAI API key in environment for OpenAI Agents SDK
# The SDK looks for OPENAI_API_KEY in os.environ, not just in settings
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Initialize database tables on startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="TutorGPT API",
    description="AI-powered book learning platform with OLIVIA tutor",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TutorGPT API - OLIVIA is ready!",
        "version": "0.1.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TutorGPT API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "tutor_agent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
