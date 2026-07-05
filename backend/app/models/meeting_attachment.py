"""Meeting Attachment model."""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import BaseModel

class MeetingAttachment(BaseModel):
    """Meeting Attachment model for tracking meeting documents."""
    __tablename__ = "meeting_attachments"
    
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)  # Path in storage system
    uploaded_by = Column(String(255), nullable=False)  # User who uploaded
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="attachments")
    
    def __repr__(self) -> str:
        return f"<MeetingAttachment(meeting_id={self.meeting_id}, filename='{self.filename}')>"
