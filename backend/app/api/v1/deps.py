"""Dependency injection for meeting endpoints."""

from sqlalchemy.orm import Session
from app.database import get_db
from app.services.meeting_service import MeetingService

async def get_meeting_service(db: Session = Depends(get_db)) -> MeetingService:
    """Get meeting service with database session."""
    return MeetingService(db)
