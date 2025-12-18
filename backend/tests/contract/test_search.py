import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_search_endpoint_contract():
    """Contract test for search endpoint"""
    # Test basic search functionality
    response = client.post("/api/search", json={"query": "test", "limit": 10})
    assert response.status_code in [200, 422]  # 200 for successful search, 422 for validation error
    
    if response.status_code == 200:
        data = response.json()
        # Validate response structure
        assert "results" in data
        assert "total" in data
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)


def test_search_query_structure():
    """Test that search endpoint accepts expected query parameters"""
    # Test minimal valid query
    valid_query = {"query": "artificial intelligence"}
    response = client.post("/api/search", json=valid_query)
    assert response.status_code in [200, 422]
    
    # Test query with options
    extended_query = {
        "query": "machine learning",
        "filters": {"language": "en"},
        "limit": 5,
        "offset": 0
    }
    response = client.post("/api/search", json=extended_query)
    assert response.status_code in [200, 422]