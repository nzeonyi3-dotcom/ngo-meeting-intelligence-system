"""Tests for meeting endpoints."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app

client = TestClient(app)

class TestMeetingCreate:
    """Test meeting creation endpoints."""
    
    def test_create_meeting_success(self):
        """Test successful meeting creation."""
        tomorrow = datetime.utcnow() + timedelta(days=1)
        meeting_data = {
            "title": "Quarterly Planning Meeting",
            "description": "Q1 strategic planning",
            "meeting_category": "strategic",
            "program_area": "Operations",
            "meeting_type": "hybrid",
            "meeting_date": tomorrow.isoformat(),
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "presenter": "John Doe",
        }
        response = client.post("/api/v1/meetings", json=meeting_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Quarterly Planning Meeting"
        assert data["presenter"] == "John Doe"
        assert "id" in data
    
    def test_create_meeting_missing_required_field(self):
        """Test meeting creation with missing required field."""
        tomorrow = datetime.utcnow() + timedelta(days=1)
        meeting_data = {
            "title": "Meeting",
            "meeting_category": "operational",
            "program_area": "Operations",
            "meeting_type": "in_person",
            "meeting_date": tomorrow.isoformat(),
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            # Missing "presenter"
        }
        response = client.post("/api/v1/meetings", json=meeting_data)
        assert response.status_code == 422
    
    def test_create_meeting_invalid_time_range(self):
        """Test meeting creation with end_time before start_time."""
        tomorrow = datetime.utcnow() + timedelta(days=1)
        meeting_data = {
            "title": "Meeting",
            "meeting_category": "operational",
            "program_area": "Operations",
            "meeting_type": "in_person",
            "meeting_date": tomorrow.isoformat(),
            "start_time": "14:00:00",
            "end_time": "10:00:00",  # Before start_time
            "presenter": "John Doe",
        }
        response = client.post("/api/v1/meetings", json=meeting_data)
        assert response.status_code == 422
    
    def test_create_meeting_invalid_google_meet_link(self):
        """Test meeting creation with invalid Google Meet link."""
        tomorrow = datetime.utcnow() + timedelta(days=1)
        meeting_data = {
            "title": "Virtual Meeting",
            "meeting_category": "operational",
            "program_area": "Operations",
            "meeting_type": "virtual",
            "meeting_date": tomorrow.isoformat(),
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "presenter": "John Doe",
            "google_meet_link": "https://zoom.us/meeting",  # Invalid
        }
        response = client.post("/api/v1/meetings", json=meeting_data)
        assert response.status_code == 422

class TestMeetingList:
    """Test meeting list endpoints."""
    
    def test_list_meetings_empty(self):
        """Test listing meetings when none exist."""
        response = client.get("/api/v1/meetings")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 0
        assert "items" in data
        assert "page" in data
        assert "page_size" in data
    
    def test_list_meetings_with_pagination(self):
        """Test meeting list pagination."""
        response = client.get("/api/v1/meetings?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page_size"] == 10
    
    def test_list_meetings_with_search(self):
        """Test meeting list with search filter."""
        response = client.get("/api/v1/meetings?search=planning")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    def test_list_meetings_with_category_filter(self):
        """Test meeting list with category filter."""
        response = client.get("/api/v1/meetings?meeting_category=strategic")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    def test_list_meetings_with_sorting(self):
        """Test meeting list with sorting."""
        response = client.get("/api/v1/meetings?sort_by=title&sort_order=asc")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

class TestMeetingDetail:
    """Test meeting detail endpoints."""
    
    def test_get_meeting_not_found(self):
        """Test getting non-existent meeting."""
        response = client.get("/api/v1/meetings/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
    
    def test_get_meeting_invalid_uuid(self):
        """Test getting meeting with invalid UUID."""
        response = client.get("/api/v1/meetings/invalid-uuid")
        assert response.status_code == 422

class TestMeetingUpdate:
    """Test meeting update endpoints."""
    
    def test_update_meeting_not_found(self):
        """Test updating non-existent meeting."""
        update_data = {"title": "Updated Title"}
        response = client.put(
            "/api/v1/meetings/00000000-0000-0000-0000-000000000000",
            json=update_data,
        )
        assert response.status_code == 404

class TestMeetingDelete:
    """Test meeting delete endpoints."""
    
    def test_delete_meeting_not_found(self):
        """Test deleting non-existent meeting."""
        response = client.delete("/api/v1/meetings/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
