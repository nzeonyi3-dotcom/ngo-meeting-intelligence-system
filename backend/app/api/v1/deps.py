"""Dependency injection."""

from sqlalchemy.orm import Session
from app.database import get_db
from app.services.info_service import InfoService

async def get_info_service() -> InfoService:
    """Get info service."""
    return InfoService()
