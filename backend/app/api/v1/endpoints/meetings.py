"""Meeting endpoints for CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.services.meeting_service import MeetingService
from app.schemas.meeting import (
    MeetingCreate,
    MeetingUpdate,
    MeetingResponse,
    MeetingListResponse,
    PaginatedMeetingResponse,
)

router = APIRouter(prefix="/api/v1/meetings", tags=["meetings"])

def get_meeting_service(db: Session = Depends(get_db)) -> MeetingService:
    """Get meeting service."""
    return MeetingService(db)

@router.post(
    "",
    response_model=MeetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new meeting",
    description="Create a new meeting with all required details",
)
async def create_meeting(
    meeting_in: MeetingCreate,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingResponse:
    """Create a new meeting.
    
    Args:
        meeting_in: Meeting creation data
        
    Returns:
        Created meeting with all details
    """
    meeting = service.create_meeting(meeting_in)
    return MeetingResponse.from_orm(meeting)

@router.get(
    "",
    response_model=PaginatedMeetingResponse,
    summary="List meetings",
    description="Get meetings with filtering, sorting, and pagination",
)
async def list_meetings(
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in title, description, presenter"),
    program_area: Optional[str] = Query(None, description="Filter by program area"),
    meeting_category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    sort_by: str = Query("meeting_date", description="Sort by field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    service: MeetingService = Depends(get_meeting_service),
) -> PaginatedMeetingResponse:
    """Get meetings with advanced filtering and pagination.
    
    Query Parameters:
        - skip: Number of items to skip (default 0)
        - limit: Number of items per page (default 100, max 1000)
        - search: Search term for title, description, presenter
        - program_area: Filter by program area
        - meeting_category: Filter by category
        - status: Filter by status
        - date_from: Filter meetings from this date
        - date_to: Filter meetings until this date
        - sort_by: Field to sort by (default: meeting_date)
        - sort_order: asc or desc (default: desc)
    """
    meetings, total = service.get_meetings(
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
    
    total_pages = (total + limit - 1) // limit
    page = (skip // limit) + 1
    
    return PaginatedMeetingResponse(
        items=[MeetingListResponse.from_orm(m) for m in meetings],
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
    )

@router.get(
    "/{meeting_id}",
    response_model=MeetingResponse,
    summary="Get meeting details",
    description="Get a specific meeting with all details",
)
async def get_meeting(
    meeting_id: str,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingResponse:
    """Get meeting by ID.
    
    Args:
        meeting_id: Meeting ID
        
    Returns:
        Meeting with all details including participants, agenda, attachments
    """
    meeting = service.get_meeting(meeting_id)
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
    return MeetingResponse.from_orm(meeting)

@router.put(
    "/{meeting_id}",
    response_model=MeetingResponse,
    summary="Update meeting",
    description="Update a meeting with new details",
)
async def update_meeting(
    meeting_id: str,
    meeting_in: MeetingUpdate,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingResponse:
    """Update a meeting.
    
    Args:
        meeting_id: Meeting ID
        meeting_in: Meeting update data
        
    Returns:
        Updated meeting
    """
    meeting = service.update_meeting(meeting_id, meeting_in)
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
    return MeetingResponse.from_orm(meeting)

@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meeting",
    description="Delete a meeting permanently",
)
async def delete_meeting(
    meeting_id: str,
    service: MeetingService = Depends(get_meeting_service),
) -> None:
    """Delete a meeting.
    
    Args:
        meeting_id: Meeting ID
    """
    success = service.delete_meeting(meeting_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting {meeting_id} not found",
        )
