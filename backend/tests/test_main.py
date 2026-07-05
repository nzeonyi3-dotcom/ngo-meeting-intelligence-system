"""Updated tests for production-ready backend."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealth:
    """Test health check endpoints."""
    
    def test_health_check_root(self):
        """Test root health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_health_check_api(self):
        """Test API health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

class TestInfo:
    """Test info endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "documentation" in data
    
    def test_info_endpoint(self):
        """Test info endpoint."""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NGO Meeting Intelligence System"
        assert data["version"] == "1.0.0"
        assert data["status"] == "ok"

class TestOpenAPI:
    """Test OpenAPI/Swagger documentation."""
    
    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "NGO Meeting Intelligence System"
        assert schema["info"]["version"] == "1.0.0"
    
    def test_docs_endpoint(self):
        """Test Swagger UI endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test ReDoc endpoint."""
        response = client.get("/redoc")
        assert response.status_code == 200
