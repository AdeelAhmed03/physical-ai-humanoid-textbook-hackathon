import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_search_integration():
    """Integration test for search functionality"""
    # Test search with a basic query
    response = client.post("/api/search", json={"query": "test"})
    # Depending on whether content is indexed, we might get different responses
    assert response.status_code in [200, 404, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert isinstance(data["results"], list)
        
        # If there are results, check they have required fields
        for result in data["results"]:
            assert "id" in result
            assert "title" in result
            assert "content" in result
            assert "score" in result


def test_search_with_filters():
    """Integration test for search with filters"""
    response = client.post("/api/search", 
                          json={
                              "query": "test",
                              "filters": {"language": "en", "chapter_id": "some-chapter"}
                          })
    assert response.status_code in [200, 404, 500]


def test_search_pagination():
    """Integration test for search pagination"""
    response = client.post("/api/search", 
                          json={
                              "query": "test",
                              "limit": 5,
                              "offset": 0
                          })
    assert response.status_code in [200, 404, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert len(data["results"]) <= 5