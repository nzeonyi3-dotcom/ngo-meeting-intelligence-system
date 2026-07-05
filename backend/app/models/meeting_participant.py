"""Meeting Participant model."""

from sqlalchemy import Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import BaseModel
from enum import Enum as PyEnum

class ParticipantRole(str, PyEnum):
    """Participant role enumeration."""
    CHAIRPERSON = "chairperson"
    PRESENTER = "presenter"
    PARTICIPANT = "participant"
    OBSERVER = "observer"
    RECORDER = "recorder"

class MeetingParticipant(BaseModel):
    """Meeting Participant model for tracking who attends meetings."""
    __tablename__ = "meeting_participants"
    
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, index=True)
    staff_id = Column(String(36), nullable=False, index=True)  # Reference to staff/user system
    role = Column(Enum(ParticipantRole), nullable=False, default=ParticipantRole.PARTICIPANT, index=True)
    attendance_required = Column(Boolean, nullable=False, default=False)
    presentation_required = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="participants")
    
    def __repr__(self) -> str:
        return f"<MeetingParticipant(meeting_id={self.meeting_id}, staff_id={self.staff_id}, role={self.role})>"
