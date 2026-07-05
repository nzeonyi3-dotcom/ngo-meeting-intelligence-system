"""Meeting service with business logic."""

from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime
from app.repositories.meeting import MeetingRepository
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingUpdate

class MeetingService:
    """Service for meeting business logic."""
    
    def __init__(self, db: Session):
        self.repository = MeetingRepository(db)
        self.db = db
    
    def create_meeting(self, meeting_in: MeetingCreate, created_by: str = "system") -> Meeting:
        """Create a new meeting."""
        meeting_data = meeting_in.dict()
        meeting_data["created_by"] = created_by
        meeting_data["updated_by"] = created_by
        return self.repository.create(meeting_data)
    
    def get_meeting(self, meeting_id: str) -> Optional[Meeting]:
        """Get meeting by ID."""
        return self.repository.get_by_id(meeting_id)
    
    def get_meetings(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        program_area: Optional[str] = None,
        meeting_category: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sort_by: str = "meeting_date",
        sort_order: str = "desc",
    ) -> Tuple[List[Meeting], int]:
        """Get meetings with filters."""
        return self.repository.get_meetings_with_filters(
            skip=skip,
            limit=limit,
            search=search,
            program_area=program_area,
            meeting_category=meeting_category,
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    
    def update_meeting(self, meeting_id: str, meeting_in: MeetingUpdate, updated_by: str = "system") -> Optional[Meeting]:
        """Update a meeting."""
        update_data = meeting_in.dict(exclude_unset=True)
        update_data["updated_by"] = updated_by
        return self.repository.update(meeting_id, update_data)
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting."""
        return self.repository.delete(meeting_id)
    
    def soft_delete_meeting(self, meeting_id: str) -> Optional[Meeting]:
        """Soft delete a meeting."""
        return self.repository.soft_delete(meeting_id)
    
    def get_upcoming_meetings(self, limit: int = 10) -> List[Meeting]:
        """Get upcoming meetings."""
        return self.repository.get_upcoming_meetings(limit)
