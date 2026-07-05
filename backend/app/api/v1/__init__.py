"""API v1 router initialization."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, info

router = APIRouter()

# Include endpoint routers
router.include_router(info.router, prefix="/info", tags=["Info"])
router.include_router(health.router, prefix="/health", tags=["Health"])
