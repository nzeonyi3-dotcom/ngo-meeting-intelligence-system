"""Main FastAPI application."""

from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.api.v1.endpoints.info import router as info_router
from app.database import engine
from app.models import Base

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(info_router)

# Health endpoint at root
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

# Create tables on startup (for development)
@app.on_event("startup")
async def startup():
    """Startup event handler."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }
