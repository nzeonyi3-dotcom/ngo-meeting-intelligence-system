"""Meeting repository with advanced queries."""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.meeting import Meeting, MeetingCategory, MeetingStatus
from app.repositories.base import BaseRepository

class MeetingRepository(BaseRepository[Meeting]):
    """Repository for Meeting model with advanced queries."""
    
    def __init__(self, db: Session):
        super().__init__(db, Meeting)
    
    def get_meetings_with_filters(
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
    ) -> tuple[List[Meeting], int]:
        """Get meetings with advanced filtering and pagination."""
        
        query = self.db.query(self.model)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.title.ilike(search_term),
                    self.model.description.ilike(search_term),
                    self.model.presenter.ilike(search_term)
                )
            )
        
        if program_area:
            query = query.filter(self.model.program_area == program_area)
        
        if meeting_category:
            query = query.filter(self.model.meeting_category == meeting_category)
        
        if status:
            query = query.filter(self.model.status == status)
        
        if date_from:
            query = query.filter(self.model.meeting_date >= date_from)
        
        if date_to:
            query = query.filter(self.model.meeting_date <= date_to)
        
        # Count total before pagination
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(self.model, sort_by, self.model.meeting_date)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        meetings = query.offset(skip).limit(limit).all()
        
        return meetings, total
    
    def get_by_title(self, title: str) -> Optional[Meeting]:
        """Get meeting by title."""
        return self.db.query(self.model).filter(self.model.title == title).first()
    
    def get_upcoming_meetings(self, limit: int = 10) -> List[Meeting]:
        """Get upcoming meetings."""
        return (
            self.db.query(self.model)
            .filter(
                and_(
                    self.model.meeting_date >= datetime.utcnow(),
                    self.model.status != MeetingStatus.CANCELLED
                )
            )
            .order_by(self.model.meeting_date)
            .limit(limit)
            .all()
        )
    
    def get_by_program_area(self, program_area: str, skip: int = 0, limit: int = 100) -> tuple[List[Meeting], int]:
        """Get meetings by program area."""
        query = self.db.query(self.model).filter(self.model.program_area == program_area)
        total = query.count()
        meetings = query.offset(skip).limit(limit).all()
        return meetings, total
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> tuple[List[Meeting], int]:
        """Get meetings by category."""
        query = self.db.query(self.model).filter(self.model.meeting_category == category)
        total = query.count()
        meetings = query.offset(skip).limit(limit).all()
        return meetings, total
