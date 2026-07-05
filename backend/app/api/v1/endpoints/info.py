"""Application info endpoints."""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def get_app_info():
    """Get application information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
    }
