from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from pydantic import BaseModel
import logging
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..utils.auth import get_current_user_from_token
from ..services.personalization_service import PersonalizationService

router = APIRouter(prefix="/personalization", tags=["personalization"])

logger = logging.getLogger(__name__)


class ChapterPreferences(BaseModel):
    difficulty_level: Optional[str] = "default"
    focus_area: Optional[str] = "all"
    examples_preference: Optional[str] = "standard"
    content_preferences: Optional[Dict] = {}


class PersonalizationResponse(BaseModel):
    message: str
    personalization_data: Optional[Dict] = None


@router.post("/chapter-preferences/{chapter_id}", response_model=PersonalizationResponse)
async def set_chapter_preferences(
    chapter_id: str,
    preferences: ChapterPreferences,
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Set chapter-specific preferences based on user background
    """
    try:
        # In a real implementation, we would save these preferences to the database
        # For now, we'll just return a success message
        logger.info(f"Updated chapter preferences for user {current_user['id']}, chapter {chapter_id}")

        return PersonalizationResponse(
            message="Chapter preferences updated successfully",
            personalization_data={
                "chapter_id": chapter_id,
                "user_id": current_user["id"],
                "preferences": preferences.dict()
            }
        )
    except Exception as e:
        logger.error(f"Error updating chapter preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update chapter preferences: {str(e)}")


@router.get("/chapter-preferences/{chapter_id}", response_model=PersonalizationResponse)
async def get_chapter_preferences(
    chapter_id: str,
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get chapter-specific preferences for the user
    """
    try:
        # In a real implementation, we would fetch preferences from the database
        # For now, we'll return default preferences based on user background
        personalization_data = PersonalizationService.get_personalized_chapter_content(
            db, current_user["id"], chapter_id, {}
        )

        return PersonalizationResponse(
            message="Chapter preferences retrieved successfully",
            personalization_data=personalization_data
        )
    except Exception as e:
        logger.error(f"Error retrieving chapter preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chapter preferences: {str(e)}")


@router.get("/learning-path", response_model=PersonalizationResponse)
async def get_learning_path_recommendation(
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get personalized learning path recommendation based on user background
    """
    try:
        recommendation = PersonalizationService.get_learning_path_recommendation(
            db, current_user["id"]
        )

        return PersonalizationResponse(
            message="Learning path recommendation retrieved successfully",
            personalization_data=recommendation
        )
    except Exception as e:
        logger.error(f"Error retrieving learning path recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve learning path: {str(e)}")


@router.post("/adapt-content", response_model=PersonalizationResponse)
async def get_content_adaptation(
    request_data: Dict,
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get content adaptation suggestions based on user background
    """
    try:
        chapter_content = request_data.get("content", "")
        chapter_id = request_data.get("chapter_id", "")

        adaptation_suggestions = PersonalizationService.get_content_adaptation_suggestions(
            db, current_user["id"], chapter_content
        )

        return PersonalizationResponse(
            message="Content adaptation suggestions retrieved successfully",
            personalization_data=adaptation_suggestions
        )
    except Exception as e:
        logger.error(f"Error retrieving content adaptation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve content adaptation: {str(e)}")