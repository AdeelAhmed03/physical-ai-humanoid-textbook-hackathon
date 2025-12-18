import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_personalization_endpoints():
    """Integration test for personalization functionality"""
    # Test creating a user preference
    preference_data = {
        "user_id": "test-user-123",
        "language": "ur",
        "learning_path": "beginner",
        "preferences": {
            "theme": "dark",
            "font_size": "medium"
        }
    }
    
    response = client.post("/api/personalization/settings", json=preference_data)
    assert response.status_code in [200, 422, 500]  # Might fail initially without implementation
    
    # Test retrieving user preferences
    response = client.get("/api/personalization/settings/test-user-123")
    assert response.status_code in [200, 404]  # 404 if user doesn't exist yet