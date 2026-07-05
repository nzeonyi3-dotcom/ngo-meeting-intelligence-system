"""Meeting model with all required fields."""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import BaseModel
from enum import Enum as PyEnum
from datetime import datetime

class MeetingCategory(str, PyEnum):
    """Meeting category enumeration."""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    TRAINING = "training"
    COORDINATION = "coordination"
    OTHER = "other"

class MeetingType(str, PyEnum):
    """Meeting type enumeration."""
    IN_PERSON = "in_person"
    VIRTUAL = "virtual"
    HYBRID = "hybrid"

class MeetingStatus(str, PyEnum):
    """Meeting status enumeration."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"

class Meeting(BaseModel):
    """Meeting model for NGO meetings."""
    __tablename__ = "meetings"
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    meeting_category = Column(Enum(MeetingCategory), nullable=False, default=MeetingCategory.OPERATIONAL)
    program_area = Column(String(255), nullable=False, index=True)
    meeting_type = Column(Enum(MeetingType), nullable=False, default=MeetingType.IN_PERSON)
    meeting_date = Column(DateTime, nullable=False, index=True)
    start_time = Column(String(8), nullable=False)  # HH:MM:SS format
    end_time = Column(String(8), nullable=False)    # HH:MM:SS format
    timezone = Column(String(63), nullable=False, default="UTC")
    venue = Column(String(255), nullable=True)
    google_meet_link = Column(String(512), nullable=True)
    chairperson = Column(String(255), nullable=True)
    presenter = Column(String(255), nullable=True)
    si_counterpart = Column(String(255), nullable=True)
    program_lead = Column(String(255), nullable=True)
    supervisor = Column(String(255), nullable=True)
    status = Column(Enum(MeetingStatus), nullable=False, default=MeetingStatus.SCHEDULED, index=True)
    is_recurring = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationships
    participants = relationship(
        "MeetingParticipant",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    agenda_items = relationship(
        "MeetingAgenda",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    attachments = relationship(
        "MeetingAttachment",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    recurrence = relationship(
        "MeetingRecurrence",
        back_populates="meeting",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Meeting(id={self.id}, title='{self.title}', date={self.meeting_date})>"
