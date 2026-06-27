"""
CodeMind FastAPI Application
Main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.config import settings
from app.api import search, demo

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level,
)

# Initialize FastAPI app
app = FastAPI(
    title="CodeMind API",
    description="Semantic code search + AI system testing agent",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting CodeMind API...")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down CodeMind API...")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "CodeMind API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "environment": settings.env,
        "debug": settings.debug,
    }


# Include API routers
app.include_router(search.router, prefix=settings.api_v1_prefix)
app.include_router(demo.router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
