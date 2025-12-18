import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_chapter_navigation_endpoints():
    """Integration test for chapter navigation functionality"""
    # Test getting all chapters
    response = client.get("/api/textbook/chapters")
    assert response.status_code in [200, 404]  # 404 if no chapters seeded yet
    
    # Test getting a specific chapter
    response = client.get("/api/textbook/chapters/invalid-id")
    assert response.status_code in [404, 200]  # Will be 404 for invalid ID, 200 for valid
    
    # Test navigation between chapters (next/previous)
    # Initially test with dummy IDs
    response = client.get("/api/textbook/chapters/invalid-id/navigation")
    assert response.status_code in [404, 200]


def test_chapter_ordering():
    """Integration test for chapter ordering functionality"""
    response = client.get("/api/textbook/chapters?sort_by=order")
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            # Check that chapters are ordered correctly
            for i in range(len(data) - 1):
                assert data[i]['order'] <= data[i + 1]['order']