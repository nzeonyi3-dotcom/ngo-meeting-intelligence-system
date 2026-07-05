"""Meeting Agenda model."""

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import BaseModel

class MeetingAgenda(BaseModel):
    """Meeting Agenda model for tracking agenda items."""
    __tablename__ = "meeting_agenda"
    
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, index=True)
    agenda_order = Column(Integer, nullable=False)  # Sequence order
    topic = Column(String(255), nullable=False, index=True)
    owner = Column(String(255), nullable=True)  # Person responsible for agenda item
    duration_minutes = Column(Integer, nullable=True)  # Duration in minutes
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="agenda_items")
    
    def __repr__(self) -> str:
        return f"<MeetingAgenda(meeting_id={self.meeting_id}, topic='{self.topic}', order={self.agenda_order})>"
