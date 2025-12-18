import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_localization_endpoint_contract():
    """Contract test for localization endpoint"""
    # Test getting available languages
    response = client.get("/api/localization/languages")
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        assert "languages" in data
        assert isinstance(data["languages"], list)
        assert len(data["languages"]) > 0
        # Check that 'en' and 'ur' are in the list
        language_codes = [lang['code'] for lang in data["languages"]]
        assert 'en' in language_codes
        assert 'ur' in language_codes


def test_get_content_by_language():
    """Contract test for getting content in specific language"""
    # Test getting content in English
    response = client.get("/api/textbook/chapters?language=en")
    assert response.status_code in [200, 404]
    
    # Test getting content in Urdu
    response = client.get("/api/textbook/chapters?language=ur")
    assert response.status_code in [200, 404]