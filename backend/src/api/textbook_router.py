from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ..db.models import Chapter as ChapterModel, ContentBlock as ContentBlockModel
from ..services.content_service import ContentService
from ..db.session import get_db


router = APIRouter(prefix="/textbook", tags=["textbook"])


class Chapter(BaseModel):
    id: int
    title: str
    content: str
    slug: str
    order: int
    language: str

    class Config:
        from_attributes = True


class ContentBlock(BaseModel):
    id: int
    chapter_id: int
    content_type: str
    content: str
    position: int

    class Config:
        from_attributes = True


class TextbookResponse(BaseModel):
    chapters: List[Chapter]


class ChapterDetailResponse(BaseModel):
    chapter: Chapter
    content_blocks: List[ContentBlock]


@router.get("/", response_model=TextbookResponse)
async def get_textbook(
    language: Optional[str] = "en",
    db: Session = Depends(get_db)
):
    """
    Retrieve the list of textbook chapters
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency
        chapters = service.get_all_chapters()

        # Convert to Pydantic models
        chapter_list = [
            Chapter(
                id=ch.id,
                title=ch.title,
                content=ch.content,
                slug=ch.slug,
                order=ch.order,
                language=ch.language
            )
            for ch in chapters
        ]

        return TextbookResponse(chapters=chapter_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()


@router.get("/{chapter_id}", response_model=ChapterDetailResponse)
async def get_chapter(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific textbook chapter with its content blocks
    """
    try:
        service = ContentService()
        service.db = db  # Inject the session from the dependency

        chapter = service.get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail=f"Chapter with id {chapter_id} not found")

        content_blocks = service.get_content_blocks_by_chapter(chapter_id)

        # Convert to Pydantic models
        chapter_model = Chapter(
            id=chapter.id,
            title=chapter.title,
            content=chapter.content,
            slug=chapter.slug,
            order=chapter.order,
            language=chapter.language
        )

        content_block_models = [
            ContentBlock(
                id=cb.id,
                chapter_id=cb.chapter_id,
                content_type=cb.content_type,
                content=cb.content,
                position=cb.position
            )
            for cb in content_blocks
        ]

        return ChapterDetailResponse(
            chapter=chapter_model,
            content_blocks=content_block_models
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close_session()