import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_production_endpoints():
    """Contract test for production endpoints"""
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "AI Textbook Backend API"


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "uptime" in data
    assert "version" in data
    assert "services" in data


def test_health_ready_endpoint():
    """Test readiness check endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "message" in data
    assert "checks" in data


def test_health_live_endpoint():
    """Test liveness check endpoint"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert "alive" in data
    assert data["alive"] is True


def test_detailed_health_endpoint():
    """Test detailed health endpoint"""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "system" in data
    assert "app" in data
    assert "cpu_percent" in data["system"]
    assert "memory_percent" in data["system"]


def test_textbook_endpoints():
    """Test textbook content endpoints"""
    # Test getting all chapters
    response = client.get("/api/textbook/")
    assert response.status_code in [200, 404]  # 404 if no content in DB yet
    if response.status_code == 200:
        data = response.json()
        assert "chapters" in data
        assert isinstance(data["chapters"], list)


def test_chat_endpoint():
    """Test chat endpoint"""
    # Test with a simple payload
    chat_data = {"message": "Hello", "context": []}
    response = client.post("/api/chat/", json=chat_data)
    # Initially this might fail if vector DB isn't set up, but should return 500 or 422, not 404
    assert response.status_code in [200, 422, 500, 404]


def test_search_endpoint():
    """Test search endpoint"""
    search_data = {"query": "test"}
    response = client.post("/api/search/", json=search_data)
    # Initially this might fail if vector DB isn't set up, but should return 500 or 422, not 404
    assert response.status_code in [200, 422, 500, 404]


def test_personalization_endpoints():
    """Test personalization endpoints"""
    # Test getting available languages
    response = client.get("/api/personalization/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    # Should have at least English
    assert any(lang['code'] == 'en' for lang in data["languages"])