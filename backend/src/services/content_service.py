from typing import List, Optional
from datetime import datetime
from ..db.models import Chapter, ContentBlock, User, UserProgress, Bookmark
from ..db.session import SessionLocal
from ..utils.logging_config import logger
from sqlalchemy.orm import Session
from pydantic import BaseModel


class ContentService:
    """
    Service for managing textbook content using Neon Postgres database
    """
    
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_all_chapters(self) -> List[Chapter]:
        """
        Retrieve all textbook chapters from the database
        """
        try:
            chapters = self.db.query(Chapter).order_by(Chapter.order).all()
            logger.info(f"Retrieved {len(chapters)} chapters from database")
            return chapters
        except Exception as e:
            logger.error(f"Error retrieving chapters: {str(e)}")
            return []

    def get_chapter_by_id(self, chapter_id: int) -> Optional[Chapter]:
        """
        Retrieve a specific chapter by its ID
        """
        try:
            chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if chapter:
                logger.info(f"Retrieved chapter with ID: {chapter_id}")
            else:
                logger.warning(f"Chapter with ID {chapter_id} not found")
            return chapter
        except Exception as e:
            logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}")
            return None

    def get_chapter_by_slug(self, slug: str) -> Optional[Chapter]:
        """
        Retrieve a specific chapter by its slug
        """
        try:
            chapter = self.db.query(Chapter).filter(Chapter.slug == slug).first()
            if chapter:
                logger.info(f"Retrieved chapter with slug: {slug}")
            else:
                logger.warning(f"Chapter with slug {slug} not found")
            return chapter
        except Exception as e:
            logger.error(f"Error retrieving chapter with slug {slug}: {str(e)}")
            return None

    def get_content_blocks_by_chapter(self, chapter_id: int) -> List[ContentBlock]:
        """
        Retrieve all content blocks for a specific chapter
        """
        try:
            content_blocks = self.db.query(ContentBlock).filter(
                ContentBlock.chapter_id == chapter_id
            ).order_by(ContentBlock.position).all()
            logger.info(f"Retrieved {len(content_blocks)} content blocks for chapter {chapter_id}")
            return content_blocks
        except Exception as e:
            logger.error(f"Error retrieving content blocks for chapter {chapter_id}: {str(e)}")
            return []

    def get_bookmarks_by_user(self, user_id: int) -> List[Bookmark]:
        """
        Retrieve all bookmarks for a specific user
        """
        try:
            bookmarks = self.db.query(Bookmark).filter(
                Bookmark.user_id == user_id
            ).all()
            logger.info(f"Retrieved {len(bookmarks)} bookmarks for user {user_id}")
            return bookmarks
        except Exception as e:
            logger.error(f"Error retrieving bookmarks for user {user_id}: {str(e)}")
            return []

    def create_bookmark(self, user_id: int, chapter_id: int, content_block_id: int, note: str = None) -> Optional[Bookmark]:
        """
        Create a new bookmark for a user
        """
        try:
            bookmark = Bookmark(
                user_id=user_id,
                chapter_id=chapter_id,
                content_block_id=content_block_id,
                note=note
            )
            self.db.add(bookmark)
            self.db.commit()
            self.db.refresh(bookmark)
            
            logger.info(f"Created bookmark for user {user_id}, chapter {chapter_id}")
            return bookmark
        except Exception as e:
            logger.error(f"Error creating bookmark: {str(e)}")
            self.db.rollback()
            return None

    def get_user_progress(self, user_id: int) -> List[UserProgress]:
        """
        Retrieve all user progress records
        """
        try:
            progress = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).all()
            logger.info(f"Retrieved {len(progress)} progress records for user {user_id}")
            return progress
        except Exception as e:
            logger.error(f"Error retrieving progress for user {user_id}: {str(e)}")
            return []

    def update_user_progress(self, user_id: int, chapter_id: int, completed: bool = True) -> Optional[UserProgress]:
        """
        Update or create user progress for a chapter
        """
        try:
            # Check if a progress record already exists
            progress = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.chapter_id == chapter_id
            ).first()

            if progress:
                # Update existing record
                progress.completed = completed
                progress.completion_date = datetime.utcnow() if completed else None
            else:
                # Create new record
                progress = UserProgress(
                    user_id=user_id,
                    chapter_id=chapter_id,
                    completed=completed,
                    completion_date=datetime.utcnow() if completed else None
                )
                self.db.add(progress)

            self.db.commit()
            logger.info(f"Updated progress for user {user_id}, chapter {chapter_id}")
            return progress
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
            self.db.rollback()
            return None

    def close_session(self):
        """
        Close the database session
        """
        self.db.close()