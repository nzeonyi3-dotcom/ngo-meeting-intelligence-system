"""Updated main.py without startup event."""

from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.api.v1.endpoints.info import router as info_router

# Setup logging first
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready NGO Meeting Intelligence System",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(info_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "documentation": "/docs",
        "schema": "/openapi.json",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
