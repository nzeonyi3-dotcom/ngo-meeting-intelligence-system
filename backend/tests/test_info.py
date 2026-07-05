"""Info endpoint tests."""

from fastapi.testclient import TestClient


def test_get_app_info(client: TestClient):
    """Test get app info endpoint."""
    response = client.get("/api/v1/info/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "NGO Meeting Intelligence System"
    assert data["version"] == "1.0.0"
    assert data["status"] == "ok"
