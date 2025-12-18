from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class EmbeddingVectorBase(BaseModel):
    content_id: str = Field(..., description="Reference to the content block")
    vector: List[float] = Field(..., description="The embedding values", min_items=10, max_items=1000)
    text: str = Field(..., description="Original text that was embedded", max_length=1000)
    chapter_id: str = Field(..., description="Reference to the chapter")


class EmbeddingVectorCreate(EmbeddingVectorBase):
    pass


class EmbeddingVectorUpdate(BaseModel):
    vector: Optional[List[float]] = Field(None, description="The embedding values", min_items=10, max_items=1000)
    text: Optional[str] = Field(None, description="Original text that was embedded", max_length=1000)


class EmbeddingVector(EmbeddingVectorBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True