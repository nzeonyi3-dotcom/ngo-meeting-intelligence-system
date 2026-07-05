"""Meeting Recurrence model."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import BaseModel
from enum import Enum as PyEnum
from datetime import datetime

class RecurrenceFrequency(str, PyEnum):
    """Recurrence frequency enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class MeetingRecurrence(BaseModel):
    """Meeting Recurrence model for tracking recurring meetings."""
    __tablename__ = "meeting_recurrence"
    
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    frequency = Column(Enum(RecurrenceFrequency), nullable=False)
    interval = Column(Integer, nullable=False, default=1)  # Repeat every N periods
    days_of_week = Column(String(13), nullable=True)  # Comma-separated: MON,WED,FRI
    end_date = Column(DateTime, nullable=True)  # When recurrence ends
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="recurrence")
    
    def __repr__(self) -> str:
        return f"<MeetingRecurrence(meeting_id={self.meeting_id}, frequency={self.frequency}, interval={self.interval})>"
