from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .chapter import Chapter


class TextbookBase(BaseModel):
    title: str = Field(..., description="Title of the textbook")
    description: str = Field(..., description="Brief description of the textbook")
    author: str = Field(..., description="Author of the textbook")
    language: str = Field(default="en", description="Primary language code (e.g., 'en', 'ur')")
    slug: str = Field(..., description="URL-friendly identifier", regex=r'^[a-z0-9-]+$')


class TextbookCreate(TextbookBase):
    pass


class TextbookUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the textbook")
    description: Optional[str] = Field(None, description="Brief description of the textbook")
    author: Optional[str] = Field(None, description="Author of the textbook")
    language: Optional[str] = Field(None, description="Primary language code (e.g., 'en', 'ur')")


class Textbook(TextbookBase):
    id: str
    chapters: List[Chapter] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True