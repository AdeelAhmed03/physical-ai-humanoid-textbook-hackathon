from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContentBlockBase(BaseModel):
    chapter_id: str = Field(..., description="Reference to the parent chapter")
    type: str = Field(..., description="Type of content (text, code, image, heading, etc.)", 
                     regex=r'^(text|code|image|heading|list|blockquote|table)$')
    content: str = Field(..., description="The actual content", max_length=1000)
    order: int = Field(..., description="Position in the chapter", ge=0)


class ContentBlockCreate(ContentBlockBase):
    pass


class ContentBlockUpdate(BaseModel):
    type: Optional[str] = Field(None, description="Type of content (text, code, image, heading, etc.)", 
                               regex=r'^(text|code|image|heading|list|blockquote|table)$')
    content: Optional[str] = Field(None, description="The actual content", max_length=1000)
    order: Optional[int] = Field(None, description="Position in the chapter", ge=0)


class ContentBlock(ContentBlockBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True