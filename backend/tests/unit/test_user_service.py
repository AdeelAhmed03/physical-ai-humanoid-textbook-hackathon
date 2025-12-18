import pytest
from src.services.user_service import UserService, UserPreference


class TestUserService:
    """Unit tests for UserService"""
    
    def setup_method(self):
        self.user_service = UserService()
        
        # Clear any existing preferences
        self.user_service.user_preferences = {}
    
    def test_set_user_language_preference(self):
        """Test setting user language preference"""
        user_id = "test_user_123"
        language = "ur"
        
        result = self.user_service.set_user_language_preference(user_id, language)
        
        assert result.user_id == user_id
        assert result.language == language
        assert user_id in self.user_service.user_preferences
    
    def test_get_user_language_preference(self):
        """Test getting user language preference"""
        user_id = "test_user_123"
        language = "ur"
        
        # Set a preference
        self.user_service.set_user_language_preference(user_id, language)
        
        # Get the preference
        result = self.user_service.get_user_language_preference(user_id)
        
        assert result == language
    
    def test_get_user_language_preference_default(self):
        """Test getting user language preference with default fallback"""
        user_id = "nonexistent_user"
        
        result = self.user_service.get_user_language_preference(user_id)
        
        assert result == "en"  # Default fallback
    
    def test_set_user_preferences(self):
        """Test setting multiple user preferences"""
        user_id = "test_user_123"
        preferences = {
            "theme": "dark",
            "font_size": "large"
        }
        
        result = self.user_service.set_user_preferences(user_id, preferences)
        
        assert result.user_id == user_id
        assert result.preferences["theme"] == "dark"
        assert result.preferences["font_size"] == "large"
    
    def test_get_user_preferences(self):
        """Test getting user preferences"""
        user_id = "test_user_123"
        preferences = {
            "theme": "dark",
            "font_size": "large"
        }
        
        # Set preferences
        self.user_service.set_user_preferences(user_id, preferences)
        
        # Get preferences
        result = self.user_service.get_user_preferences(user_id)
        
        assert result.user_id == user_id
        assert result.preferences["theme"] == "dark"
        assert result.preferences["font_size"] == "large"
    
    def test_get_available_languages(self):
        """Test getting available languages"""
        languages = self.user_service.get_available_languages()
        
        assert len(languages) == 2
        assert {"code": "en", "name": "English"} in languages
        assert {"code": "ur", "name": "Urdu"} in languages