from pydantic import BaseSettings, validator
from typing import Optional
import os


class Settings(BaseSettings):
    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Server Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    log_level: str = "INFO"
    
    # Security Settings
    secret_key: str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Performance Settings
    max_content_length: int = 1000
    embedding_dimension: int = 384
    
    # Rate Limiting (requests per window)
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # in seconds
    
    # API Base URL for frontend communication
    api_base_url: str = "http://localhost:8000"
    
    @validator('port')
    def validate_port(cls, v):
        if v < 1 or v > 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @validator('qdrant_url')
    def validate_qdrant_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Qdrant URL must start with http:// or https://')
        return v
    
    @validator('embedding_dimension')
    def validate_embedding_dimension(cls, v):
        if v <= 0:
            raise ValueError('Embedding dimension must be positive')
        return v

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")  # Use .env by default, or specified file
        env_file_encoding = 'utf-8'


# Create a single instance of settings
settings = Settings()


def validate_environment():
    """Validate the environment configuration"""
    errors = []
    
    # Validate required settings
    if not settings.qdrant_url:
        errors.append("QDRANT_URL is required")
    
    # Add additional validations as needed
    if settings.secret_key == "dev-secret-key-change-in-production":
        errors.append("SECRET_KEY should be changed for production")
    
    if errors:
        raise ValueError(f"Configuration errors: {'; '.join(errors)}")


# Validate when module is loaded
validate_environment()