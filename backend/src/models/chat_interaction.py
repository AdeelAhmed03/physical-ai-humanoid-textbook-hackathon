from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatInteractionBase(BaseModel):
    session_id: str = Field(..., description="Reference to the user session")
    user_input: str = Field(..., description="The question asked by the user", max_length=2000)
    response: str = Field(..., description="The AI's response", max_length=5000)
    context_used: Optional[List[str]] = Field(default=[], description="Chapter/section references used in the response")


class ChatInteractionCreate(ChatInteractionBase):
    pass


class ChatInteractionUpdate(BaseModel):
    response: Optional[str] = Field(None, description="The AI's response", max_length=5000)
    context_used: Optional[List[str]] = Field(None, description="Chapter/section references used in the response")


class ChatInteraction(ChatInteractionBase):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True