"""Meeting schemas for request/response validation."""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.models.meeting import MeetingCategory, MeetingType, MeetingStatus
from app.models.meeting_participant import ParticipantRole

class MeetingParticipantSchema(BaseModel):
    """Schema for meeting participant."""
    id: Optional[str] = None
    staff_id: str = Field(..., min_length=1, description="Staff ID")
    role: ParticipantRole = Field(default=ParticipantRole.PARTICIPANT, description="Participant role")
    attendance_required: bool = Field(default=False, description="Is attendance required")
    presentation_required: bool = Field(default=False, description="Is presentation required")
    
    class Config:
        from_attributes = True

class MeetingAgendaSchema(BaseModel):
    """Schema for meeting agenda item."""
    id: Optional[str] = None
    agenda_order: int = Field(..., ge=1, description="Order in agenda")
    topic: str = Field(..., min_length=1, max_length=255, description="Agenda topic")
    owner: Optional[str] = Field(None, max_length=255, description="Person responsible")
    duration_minutes: Optional[int] = Field(None, ge=1, le=480, description="Duration in minutes")
    
    class Config:
        from_attributes = True

class MeetingAttachmentSchema(BaseModel):
    """Schema for meeting attachment."""
    id: Optional[str] = None
    filename: str = Field(..., min_length=1, max_length=255, description="File name")
    storage_path: str = Field(..., min_length=1, max_length=512, description="Storage path")
    uploaded_by: str = Field(..., min_length=1, max_length=255, description="Uploaded by user")
    
    class Config:
        from_attributes = True

class MeetingRecurrenceSchema(BaseModel):
    """Schema for meeting recurrence."""
    id: Optional[str] = None
    frequency: str = Field(..., description="Recurrence frequency")
    interval: int = Field(default=1, ge=1, le=365, description="Repeat interval")
    days_of_week: Optional[str] = Field(None, max_length=13, description="Days: MON,WED,FRI")
    end_date: Optional[datetime] = Field(None, description="Recurrence end date")
    
    class Config:
        from_attributes = True

class MeetingCreate(BaseModel):
    """Schema for creating a meeting."""
    title: str = Field(..., min_length=3, max_length=255, description="Meeting title")
    description: Optional[str] = Field(None, max_length=2000, description="Meeting description")
    meeting_category: MeetingCategory = Field(default=MeetingCategory.OPERATIONAL, description="Meeting category")
    program_area: str = Field(..., min_length=1, max_length=255, description="Program area")
    meeting_type: MeetingType = Field(default=MeetingType.IN_PERSON, description="Meeting type")
    meeting_date: datetime = Field(..., description="Meeting date and time")
    start_time: str = Field(..., pattern=r'^\d{2}:\d{2}:\d{2}$', description="Start time HH:MM:SS")
    end_time: str = Field(..., pattern=r'^\d{2}:\d{2}:\d{2}$', description="End time HH:MM:SS")
    timezone: str = Field(default="UTC", max_length=63, description="Timezone")
    venue: Optional[str] = Field(None, max_length=255, description="Meeting venue")
    google_meet_link: Optional[str] = Field(None, max_length=512, description="Google Meet link")
    chairperson: Optional[str] = Field(None, max_length=255, description="Chairperson name")
    presenter: str = Field(..., min_length=1, max_length=255, description="Presenter name")
    si_counterpart: Optional[str] = Field(None, max_length=255, description="SI counterpart")
    program_lead: Optional[str] = Field(None, max_length=255, description="Program lead")
    supervisor: Optional[str] = Field(None, max_length=255, description="Supervisor")
    is_recurring: bool = Field(default=False, description="Is meeting recurring")
    
    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        """Validate that end_time is after start_time."""
        if 'start_time' in values:
            start = values['start_time']
            if v <= start:
                raise ValueError('End time must be after start time')
        return v
    
    @validator('google_meet_link')
    def validate_google_meet_link(cls, v):
        """Validate Google Meet URL format."""
        if v and not v.startswith(('https://meet.google.com/', 'http://meet.google.com/')):
            raise ValueError('Invalid Google Meet link format')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Quarterly Planning Meeting",
                "description": "Q1 strategic planning session",
                "meeting_category": "strategic",
                "program_area": "Operations",
                "meeting_type": "hybrid",
                "meeting_date": "2024-01-15T10:00:00Z",
                "start_time": "10:00:00",
                "end_time": "12:00:00",
                "timezone": "UTC",
                "presenter": "John Doe",
                "program_lead": "Jane Smith"
            }
        }

class MeetingUpdate(BaseModel):
    """Schema for updating a meeting."""
    title: Optional[str] = Field(None, min_length=3, max_length=255, description="Meeting title")
    description: Optional[str] = Field(None, max_length=2000, description="Meeting description")
    meeting_category: Optional[MeetingCategory] = Field(None, description="Meeting category")
    program_area: Optional[str] = Field(None, min_length=1, max_length=255, description="Program area")
    meeting_type: Optional[MeetingType] = Field(None, description="Meeting type")
    meeting_date: Optional[datetime] = Field(None, description="Meeting date")
    start_time: Optional[str] = Field(None, pattern=r'^\d{2}:\d{2}:\d{2}$', description="Start time")
    end_time: Optional[str] = Field(None, pattern=r'^\d{2}:\d{2}:\d{2}$', description="End time")
    timezone: Optional[str] = Field(None, max_length=63, description="Timezone")
    venue: Optional[str] = Field(None, max_length=255, description="Meeting venue")
    google_meet_link: Optional[str] = Field(None, max_length=512, description="Google Meet link")
    chairperson: Optional[str] = Field(None, max_length=255, description="Chairperson")
    presenter: Optional[str] = Field(None, min_length=1, max_length=255, description="Presenter")
    si_counterpart: Optional[str] = Field(None, max_length=255, description="SI counterpart")
    program_lead: Optional[str] = Field(None, max_length=255, description="Program lead")
    supervisor: Optional[str] = Field(None, max_length=255, description="Supervisor")
    status: Optional[MeetingStatus] = Field(None, description="Meeting status")
    is_recurring: Optional[bool] = Field(None, description="Is meeting recurring")
    is_active: Optional[bool] = Field(None, description="Is meeting active")
    
    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        """Validate that end_time is after start_time."""
        if v and 'start_time' in values and values['start_time']:
            if v <= values['start_time']:
                raise ValueError('End time must be after start time')
        return v
    
    @validator('google_meet_link')
    def validate_google_meet_link(cls, v):
        """Validate Google Meet URL format."""
        if v and not v.startswith(('https://meet.google.com/', 'http://meet.google.com/')):
            raise ValueError('Invalid Google Meet link format')
        return v

class MeetingResponse(BaseModel):
    """Schema for meeting response."""
    id: str = Field(..., description="Meeting ID")
    title: str = Field(..., description="Meeting title")
    description: Optional[str] = Field(None, description="Meeting description")
    meeting_category: MeetingCategory = Field(..., description="Meeting category")
    program_area: str = Field(..., description="Program area")
    meeting_type: MeetingType = Field(..., description="Meeting type")
    meeting_date: datetime = Field(..., description="Meeting date")
    start_time: str = Field(..., description="Start time")
    end_time: str = Field(..., description="End time")
    timezone: str = Field(..., description="Timezone")
    venue: Optional[str] = Field(None, description="Meeting venue")
    google_meet_link: Optional[str] = Field(None, description="Google Meet link")
    chairperson: Optional[str] = Field(None, description="Chairperson")
    presenter: str = Field(..., description="Presenter")
    si_counterpart: Optional[str] = Field(None, description="SI counterpart")
    program_lead: Optional[str] = Field(None, description="Program lead")
    supervisor: Optional[str] = Field(None, description="Supervisor")
    status: MeetingStatus = Field(..., description="Meeting status")
    is_recurring: bool = Field(..., description="Is meeting recurring")
    is_active: bool = Field(..., description="Is meeting active")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")
    created_by: Optional[str] = Field(None, description="Created by")
    updated_by: Optional[str] = Field(None, description="Updated by")
    participants: List[MeetingParticipantSchema] = Field(default_factory=list, description="Meeting participants")
    agenda_items: List[MeetingAgendaSchema] = Field(default_factory=list, description="Agenda items")
    attachments: List[MeetingAttachmentSchema] = Field(default_factory=list, description="Attachments")
    recurrence: Optional[MeetingRecurrenceSchema] = Field(None, description="Recurrence info")
    
    class Config:
        from_attributes = True

class MeetingListResponse(BaseModel):
    """Schema for meeting list response."""
    id: str = Field(..., description="Meeting ID")
    title: str = Field(..., description="Meeting title")
    meeting_category: MeetingCategory = Field(..., description="Meeting category")
    program_area: str = Field(..., description="Program area")
    meeting_type: MeetingType = Field(..., description="Meeting type")
    meeting_date: datetime = Field(..., description="Meeting date")
    start_time: str = Field(..., description="Start time")
    presenter: str = Field(..., description="Presenter")
    status: MeetingStatus = Field(..., description="Meeting status")
    is_recurring: bool = Field(..., description="Is meeting recurring")
    created_at: datetime = Field(..., description="Created at")
    
    class Config:
        from_attributes = True

class PaginatedMeetingResponse(BaseModel):
    """Schema for paginated meeting list response."""
    items: List[MeetingListResponse] = Field(..., description="Meeting items")
    total: int = Field(..., ge=0, description="Total count")
    page: int = Field(..., ge=1, description="Current page")
    page_size: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total pages")
