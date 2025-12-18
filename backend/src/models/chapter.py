from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChapterBase(BaseModel):
    title: str = Field(..., description="Title of the chapter")
    content: str = Field(..., description="Full text content of the chapter", max_length=50000)
    slug: str = Field(..., description="URL-friendly identifier", regex=r'^[a-z0-9-]+$')
    order: int = Field(..., description="Chapter's position in the textbook sequence", ge=1)
    language: str = Field(default="en", description="Language code (e.g., 'en', 'ur')")
    metadata: Optional[dict] = Field(default={}, description="Additional information about the chapter")


class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the chapter")
    content: Optional[str] = Field(None, description="Full text content of the chapter", max_length=50000)
    slug: Optional[str] = Field(None, description="URL-friendly identifier", regex=r'^[a-z0-9-]+$')
    order: Optional[int] = Field(None, description="Chapter's position in the textbook sequence", ge=1)
    language: Optional[str] = Field(None, description="Language code (e.g., 'en', 'ur')")
    metadata: Optional[dict] = Field(None, description="Additional information about the chapter")


class Chapter(ChapterBase):
    id: str
    textbook_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True