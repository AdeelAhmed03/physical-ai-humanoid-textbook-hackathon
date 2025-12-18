from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from ..db.models import Bookmark as BookmarkModel, UserProgress as UserProgressModel, ChapterPreference
from ..services.content_service import ContentService
from ..services.translation_service import translation_service
from ..db.session import get_db
from ..utils.auth import oauth2_scheme, get_current_user_from_token
import json


router = APIRouter(prefix="/user", tags=["user"])


class BookmarkBase(BaseModel):
    user_id: int
    chapter_id: int
    content_block_id: int
    note: Optional[str] = None


class BookmarkCreate(BookmarkBase):
    pass


class Bookmark(BookmarkBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserProgressBase(BaseModel):
    user_id: int
    chapter_id: int
    completed: bool = False
    time_spent: Optional[int] = 0  # in seconds


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase):
    id: int
    completion_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookmarkResponse(BaseModel):
    bookmarks: List[Bookmark]


class ProgressResponse(BaseModel):
    progress: List[UserProgress]


@router.get("/bookmarks/{user_id}", response_model=BookmarkResponse)
async def get_user_bookmarks(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all bookmarks for a specific user
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency

        bookmarks = service.get_bookmarks_by_user(user_id)

        # Convert to Pydantic models
        bookmark_list = [
            Bookmark(
                id=bookmark.id,
                user_id=bookmark.user_id,
                chapter_id=bookmark.chapter_id,
                content_block_id=bookmark.content_block_id,
                note=bookmark.note,
                created_at=bookmark.created_at
            )
            for bookmark in bookmarks
        ]

        return BookmarkResponse(bookmarks=bookmark_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()


@router.post("/bookmarks", response_model=Bookmark)
async def create_bookmark(
    bookmark_data: BookmarkCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new bookmark for a user
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency

        new_bookmark = service.create_bookmark(
            user_id=bookmark_data.user_id,
            chapter_id=bookmark_data.chapter_id,
            content_block_id=bookmark_data.content_block_id,
            note=bookmark_data.note
        )

        if not new_bookmark:
            raise HTTPException(status_code=500, detail="Failed to create bookmark")

        # Convert to Pydantic model
        result = Bookmark(
            id=new_bookmark.id,
            user_id=new_bookmark.user_id,
            chapter_id=new_bookmark.chapter_id,
            content_block_id=new_bookmark.content_block_id,
            note=new_bookmark.note,
            created_at=new_bookmark.created_at
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()


@router.get("/progress/{user_id}", response_model=ProgressResponse)
async def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve all progress records for a specific user
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency

        progress_records = service.get_user_progress(user_id)

        # Convert to Pydantic models
        progress_list = [
            UserProgress(
                id=progress.id,
                user_id=progress.user_id,
                chapter_id=progress.chapter_id,
                completed=progress.completed,
                time_spent=progress.time_spent,
                completion_date=progress.completion_date
            )
            for progress in progress_records
        ]

        return ProgressResponse(progress=progress_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()


@router.post("/progress", response_model=UserProgress)
async def update_user_progress(
    progress_data: UserProgressCreate,
    db: Session = Depends(get_db)
):
    """
    Update or create user progress for a chapter
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency

        updated_progress = service.update_user_progress(
            user_id=progress_data.user_id,
            chapter_id=progress_data.chapter_id,
            completed=progress_data.completed
        )

        if not updated_progress:
            raise HTTPException(status_code=500, detail="Failed to update progress")

        # Convert to Pydantic model
        result = UserProgress(
            id=updated_progress.id,
            user_id=updated_progress.user_id,
            chapter_id=updated_progress.chapter_id,
            completed=updated_progress.completed,
            time_spent=updated_progress.time_spent,
            completion_date=updated_progress.completion_date
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()


class ChapterPreferenceRequest(BaseModel):
    preferences: Dict[str, Any]


class ChapterPreferenceResponse(BaseModel):
    chapter_id: str
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


@router.get("/chapter-preferences/{chapter_id}", response_model=Optional[ChapterPreferenceResponse])
async def get_chapter_preferences(
    chapter_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Retrieve chapter preferences for the current user
    """
    user = get_current_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        # Find existing preferences for this user and chapter
        preference = db.query(ChapterPreference).filter(
            ChapterPreference.user_id == user.id,
            ChapterPreference.chapter_id == chapter_id
        ).first()

        if not preference:
            return None

        # Parse the JSON preferences
        preferences = json.loads(preference.preferences) if preference.preferences else {}

        return ChapterPreferenceResponse(
            chapter_id=preference.chapter_id,
            preferences=preferences,
            created_at=preference.created_at,
            updated_at=preference.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chapter-preferences/{chapter_id}", response_model=ChapterPreferenceResponse)
async def set_chapter_preferences(
    chapter_id: str,
    preference_data: ChapterPreferenceRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Set chapter preferences for the current user
    """
    user = get_current_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        # Check if preferences already exist for this user and chapter
        existing_preference = db.query(ChapterPreference).filter(
            ChapterPreference.user_id == user.id,
            ChapterPreference.chapter_id == chapter_id
        ).first()

        if existing_preference:
            # Update existing preferences
            existing_preference.preferences = json.dumps(preference_data.preferences)
            existing_preference.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_preference)
            preference = existing_preference
        else:
            # Create new preferences
            preference = ChapterPreference(
                user_id=user.id,
                chapter_id=chapter_id,
                preferences=json.dumps(preference_data.preferences)
            )
            db.add(preference)
            db.commit()
            db.refresh(preference)

        # Parse the JSON preferences
        preferences = json.loads(preference.preferences) if preference.preferences else {}

        return ChapterPreferenceResponse(
            chapter_id=preference.chapter_id,
            preferences=preferences,
            created_at=preference.created_at,
            updated_at=preference.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TranslateChapterRequest(BaseModel):
    chapter_id: str
    content: str
    target_language: str = "ur"


class TranslateChapterResponse(BaseModel):
    chapter_id: str
    original_content: str
    translated_content: str
    target_language: str


@router.post("/translate-chapter", response_model=TranslateChapterResponse)
async def translate_chapter(
    translate_request: TranslateChapterRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Translate chapter content to the target language (Urdu)
    """
    user = get_current_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        # For now, using a placeholder translation
        # In a real implementation, this would call the translation service
        # which could use OpenAI or other translation APIs
        translated_content = await translation_service.translate_text_async(
            translate_request.content,
            translate_request.target_language
        )

        # If translation fails or returns None, return original content
        if translated_content is None:
            translated_content = translate_request.content

        return TranslateChapterResponse(
            chapter_id=translate_request.chapter_id,
            original_content=translate_request.content,
            translated_content=translated_content,
            target_language=translate_request.target_language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))