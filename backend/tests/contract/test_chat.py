"""
Contract test for chat endpoint in backend/tests/contract/test_chat.py
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_chat_endpoint_contract():
    """
    Test that the chat endpoint follows the expected contract
    """
    # Test with a basic query
    response = client.post(
        "/chat/",
        json={
            "query": "What is Physical AI?",
            "session_id": "test-session-123",
            "language": "en"
        }
    )
    
    # Should return 200 OK
    assert response.status_code == 200
    
    # Response should have the expected structure
    data = response.json()
    assert "response" in data
    assert "sources" in data
    assert "session_id" in data
    
    # Response should be a string
    assert isinstance(data["response"], str)
    
    # Sources should be a list
    assert isinstance(data["sources"], list)
    
    # Session ID should match what we sent or be generated
    assert data["session_id"] == "test-session-123" or isinstance(data["session_id"], str)


def test_chat_endpoint_missing_query():
    """
    Test that the chat endpoint handles missing query properly
    """
    response = client.post(
        "/chat/",
        json={
            "session_id": "test-session-123"
        }
    )
    
    # Should return 422 validation error since query is required
    assert response.status_code == 422


def test_chat_endpoint_empty_query():
    """
    Test that the chat endpoint handles empty query properly
    """
    response = client.post(
        "/chat/",
        json={
            "query": "",
            "session_id": "test-session-123"
        }
    )
    
    # Should return 400 since empty query is not allowed
    assert response.status_code == 400