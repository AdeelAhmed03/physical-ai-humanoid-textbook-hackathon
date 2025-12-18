import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.content_service import ContentService
from src.models.chapter import Chapter
from datetime import datetime


class TestContentService:
    """Unit tests for ContentService"""
    
    def setup_method(self):
        self.content_service = ContentService()
        
        # Clear any existing chapters
        self.content_service.chapters = {}
    
    def test_create_chapter(self):
        """Test creating a chapter"""
        chapter = self.content_service.create_chapter(
            title="Test Chapter",
            content="This is a test chapter.",
            slug="test-chapter",
            order=1
        )
        
        assert chapter.title == "Test Chapter"
        assert chapter.content == "This is a test chapter."
        assert chapter.slug == "test-chapter"
        assert chapter.order == 1
        assert chapter.id in self.content_service.chapters
    
    def test_get_chapter_by_id(self):
        """Test retrieving a chapter by ID"""
        chapter = self.content_service.create_chapter(
            title="Test Chapter",
            content="This is a test chapter.",
            slug="test-chapter",
            order=1
        )
        
        retrieved_chapter = self.content_service.get_chapter_by_id(chapter.id)
        assert retrieved_chapter.id == chapter.id
        assert retrieved_chapter.title == chapter.title
    
    def test_update_chapter(self):
        """Test updating a chapter"""
        chapter = self.content_service.create_chapter(
            title="Test Chapter",
            content="This is a test chapter.",
            slug="test-chapter",
            order=1
        )
        
        updated_chapter = self.content_service.update_chapter(
            chapter.id,
            title="Updated Chapter",
            content="Updated content."
        )
        
        assert updated_chapter.title == "Updated Chapter"
        assert updated_chapter.content == "Updated content."
    
    def test_delete_chapter(self):
        """Test deleting a chapter"""
        chapter = self.content_service.create_chapter(
            title="Test Chapter",
            content="This is a test chapter.",
            slug="test-chapter",
            order=1
        )
        
        result = self.content_service.delete_chapter(chapter.id)
        assert result is True
        assert chapter.id not in self.content_service.chapters
    
    def test_get_all_chapters(self):
        """Test retrieving all chapters"""
        # Create multiple chapters
        chapter1 = self.content_service.create_chapter(
            title="Chapter 1",
            content="Content 1",
            slug="chapter-1",
            order=1
        )
        
        chapter2 = self.content_service.create_chapter(
            title="Chapter 2",
            content="Content 2",
            slug="chapter-2",
            order=2
        )
        
        chapters = self.content_service.get_all_chapters()
        assert len(chapters) == 2
        assert chapter1.id in [ch.id for ch in chapters]
        assert chapter2.id in [ch.id for ch in chapters]
    
    def test_search_chapters(self):
        """Test searching chapters"""
        chapter1 = self.content_service.create_chapter(
            title="AI Fundamentals",
            content="This chapter covers artificial intelligence basics.",
            slug="ai-fundamentals",
            order=1
        )
        
        chapter2 = self.content_service.create_chapter(
            title="Robotics",
            content="This chapter covers robotics concepts.",
            slug="robotics",
            order=2
        )
        
        # Search for content containing "artificial"
        results = self.content_service.search_chapters("artificial")
        assert len(results) == 1
        assert results[0].id == chapter1.id