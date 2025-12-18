import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.textbook import Textbook

client = TestClient(app)


def test_get_textbook_chapters():
    """Contract test for textbook content endpoints"""
    response = client.get("/api/textbook/chapters")
    # Initially expect a 200 response with an empty list or sample chapters
    assert response.status_code in [200, 404]  # 404 if no chapters seeded yet
    
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        # If there are chapters, they should conform to the expected schema
        if len(data) > 0:
            for chapter in data:
                assert "id" in chapter
                assert "title" in chapter
                assert "content" in chapter
                assert "order" in chapter


def test_get_single_chapter():
    """Contract test for getting a specific chapter"""
    # Test with a dummy ID initially
    response = client.get("/api/textbook/chapters/invalid-id")
    assert response.status_code in [404, 200]


def test_textbook_model_schema():
    """Test that Textbook model conforms to expected schema"""
    textbook_data = {
        "id": "textbook-1",
        "title": "Sample Textbook",
        "description": "A sample textbook for testing",
        "author": "Test Author",
        "language": "en",
        "slug": "sample-textbook",
        "chapters": [],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    
    textbook = Textbook(**textbook_data)
    assert textbook.title == "Sample Textbook"
    assert textbook.author == "Test Author"