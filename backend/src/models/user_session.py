from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class UserSessionBase(BaseModel):
    user_id: Optional[str] = Field(None, description="User identifier (optional, for personalization)")
    preferences: Optional[Dict] = Field(default={}, description="User's personalization settings")
    language_preference: str = Field(default="en", description="User's preferred language")


class UserSessionCreate(UserSessionBase):
    pass


class UserSessionUpdate(BaseModel):
    preferences: Optional[Dict] = Field(None, description="User's personalization settings")
    language_preference: Optional[str] = Field(None, description="User's preferred language")


class UserSession(UserSessionBase):
    id: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True