import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_response_format():
    """Test that health endpoint returns expected format"""
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "uptime" in data
    assert "version" in data
    assert "services" in data
    
    # Validate types
    assert isinstance(data["status"], str)
    assert isinstance(data["uptime"], float)
    assert isinstance(data["version"], str)
    assert isinstance(data["services"], dict)


def test_health_ready_response():
    """Test that ready endpoint returns expected format"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert "ready" in data
    assert "message" in data
    assert "checks" in data
    
    # Validate types
    assert isinstance(data["ready"], bool)
    assert isinstance(data["message"], str)
    assert isinstance(data["checks"], dict)


def test_health_live_response():
    """Test that live endpoint returns expected format"""
    response = client.get("/health/live")
    assert response.status_code == 200
    
    data = response.json()
    assert "alive" in data
    assert "message" in data
    
    # Validate types
    assert isinstance(data["alive"], bool)
    assert isinstance(data["message"], str)


def test_detailed_health_response():
    """Test that detailed health endpoint returns expected format"""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "system" in data
    assert "app" in data
    
    system_data = data["system"]
    assert "cpu_percent" in system_data
    assert "memory_percent" in system_data
    assert "disk_usage_percent" in system_data
    assert "process_count" in system_data


def test_health_status_values():
    """Test that health status values are valid"""
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy", "degraded"]


def test_ready_status_logic():
    """Test readiness status logic"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    # If ready is True, message should indicate application is ready
    if data["ready"]:
        assert "ready" in data["message"].lower()
    else:
        assert "not ready" in data["message"].lower() or "error" in data["message"].lower()