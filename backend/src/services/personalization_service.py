from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..db.models import User, Chapter, UserProgress
from ..db.session import get_db


class PersonalizationService:
    """Service to handle content personalization based on user background."""

    @staticmethod
    def get_personalized_chapter_content(
        db: Session,
        user_id: int,
        chapter_id: str,
        content_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get personalized chapter content based on user background and preferences.

        Args:
            db: Database session
            user_id: User ID
            chapter_id: Chapter identifier
            content_preferences: User's content preferences

        Returns:
            Dictionary with personalized content options
        """
        # Get user information
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"content": "default", "options": {}}

        # Create personalization recommendations based on user background
        personalization_options = {}

        # Adjust difficulty based on user experience
        if user.experience_level:
            if "advanced" in user.experience_level.lower():
                personalization_options["skip_basics"] = True
                personalization_options["add_advanced_examples"] = True
            elif "beginner" in user.experience_level.lower():
                personalization_options["add_basics"] = True
                personalization_options["simplified_explanation"] = True

        # Adjust focus based on user background
        if user.software_background and not user.hardware_background:
            personalization_options["code_focus"] = True
            personalization_options["implementation_details"] = True
        elif not user.software_background and user.hardware_background:
            personalization_options["theory_focus"] = True
            personalization_options["conceptual_explanation"] = True
        elif user.software_background and user.hardware_background:
            personalization_options["balanced_approach"] = True

        # Apply user's specific preferences
        if content_preferences:
            personalization_options.update(content_preferences)

        return {
            "user_background": {
                "software_background": user.software_background,
                "hardware_background": user.hardware_background,
                "experience_level": user.experience_level
            },
            "personalization_options": personalization_options,
            "recommended_difficulty": user.experience_level or "default"
        }

    @staticmethod
    def get_learning_path_recommendation(
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Get recommended learning path based on user background.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Dictionary with learning path recommendation
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"path": "standard", "reason": "User not found"}

        # Determine learning path based on user background
        if user.experience_level and "beginner" in user.experience_level.lower():
            path = "beginner"
            reason = "Based on your beginner experience level"
        elif user.experience_level and "advanced" in user.experience_level.lower():
            path = "advanced"
            reason = "Based on your advanced experience level"
        elif user.software_background and not user.hardware_background:
            path = "software-focused"
            reason = "Based on your software background"
        elif not user.software_background and user.hardware_background:
            path = "hardware-focused"
            reason = "Based on your hardware background"
        else:
            path = "standard"
            reason = "General recommendation"

        return {
            "path": path,
            "reason": reason,
            "suggested_order": PersonalizationService._get_suggested_chapter_order(path)
        }

    @staticmethod
    def _get_suggested_chapter_order(path: str) -> List[str]:
        """Get suggested chapter order based on learning path."""
        if path == "beginner":
            return [
                "introduction", "basics", "intermediate", "advanced",
                "applications", "conclusion"
            ]
        elif path == "advanced":
            return [
                "advanced", "applications", "introduction", "basics",
                "intermediate", "conclusion"
            ]
        elif path == "software-focused":
            return [
                "introduction", "software-aspects", "applications",
                "basics", "advanced", "conclusion"
            ]
        elif path == "hardware-focused":
            return [
                "introduction", "hardware-aspects", "applications",
                "basics", "advanced", "conclusion"
            ]
        else:
            return [
                "introduction", "basics", "intermediate", "advanced",
                "applications", "conclusion"
            ]

    @staticmethod
    def get_content_adaptation_suggestions(
        db: Session,
        user_id: int,
        chapter_content: str
    ) -> Dict[str, Any]:
        """
        Get suggestions for adapting chapter content based on user background.

        Args:
            db: Database session
            user_id: User ID
            chapter_content: Original chapter content

        Returns:
            Dictionary with content adaptation suggestions
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"adapted_content": chapter_content, "changes": []}

        suggestions = []

        # Generate adaptation suggestions based on user background
        if user.experience_level and "beginner" in user.experience_level.lower():
            suggestions.append({
                "type": "add_context",
                "description": "Add more basic explanations and context"
            })
        elif user.experience_level and "advanced" in user.experience_level.lower():
            suggestions.append({
                "type": "add_depth",
                "description": "Add more advanced concepts and details"
            })

        if user.software_background and not user.hardware_background:
            suggestions.append({
                "type": "add_code_examples",
                "description": "Include more code examples and implementation details"
            })
        elif not user.software_background and user.hardware_background:
            suggestions.append({
                "type": "add_theory",
                "description": "Include more theoretical explanations"
            })

        return {
            "original_content": chapter_content,
            "suggestions": suggestions,
            "user_profile": {
                "experience_level": user.experience_level,
                "software_background": bool(user.software_background),
                "hardware_background": bool(user.hardware_background)
            }
        }