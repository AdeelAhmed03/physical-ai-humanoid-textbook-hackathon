from typing import Dict, Optional, List
from ..models.user_session import UserSession
from ..utils.logging_config import logger
import uuid
from datetime import datetime, timedelta


class UserPreference:
    """Represents a user's preferences including language settings"""
    
    def __init__(self, user_id: str, language: str = "en", learning_path: str = "standard", 
                 preferences: Optional[Dict] = None):
        self.user_id = user_id
        self.language = language
        self.learning_path = learning_path
        self.preferences = preferences or {}
        self.updated_at = datetime.utcnow()


class UserService:
    """
    Service for managing user preferences and sessions
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use in-memory storage for demonstration
        self.user_preferences: Dict[str, UserPreference] = {}
    
    def set_user_language_preference(self, user_id: str, language: str) -> UserPreference:
        """Set the language preference for a user"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreference(user_id=user_id, language=language)
        else:
            self.user_preferences[user_id].language = language
            self.user_preferences[user_id].updated_at = datetime.utcnow()
        
        logger.info(f"Set language preference for user {user_id} to {language}")
        return self.user_preferences[user_id]
    
    def get_user_language_preference(self, user_id: str) -> str:
        """Get the language preference for a user, defaulting to 'en'"""
        if user_id in self.user_preferences:
            return self.user_preferences[user_id].language
        return "en"  # Default to English
    
    def set_user_preferences(self, user_id: str, preferences: Dict) -> UserPreference:
        """Set multiple preferences for a user"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreference(user_id=user_id)
        
        # Update the preferences
        self.user_preferences[user_id].preferences.update(preferences)
        self.user_preferences[user_id].updated_at = datetime.utcnow()
        
        logger.info(f"Updated preferences for user {user_id}: {preferences.keys()}")
        return self.user_preferences[user_id]
    
    def get_user_preferences(self, user_id: str) -> Optional[UserPreference]:
        """Get all preferences for a user"""
        return self.user_preferences.get(user_id)
    
    def get_available_languages(self) -> List[Dict[str, str]]:
        """Get list of available languages for the application"""
        return [
            {"code": "en", "name": "English"},
            {"code": "ur", "name": "Urdu"}
        ]
    
    def create_user_session(self, user_id: str, session_data: Optional[Dict] = None) -> UserSession:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        session = UserSession(
            id=session_id,
            user_id=user_id,
            session_data=session_data or {},
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=24)  # 24-hour session
        )
        logger.info(f"Created session {session_id} for user {user_id}")
        return session


# Global instance of the UserService
user_service = UserService()