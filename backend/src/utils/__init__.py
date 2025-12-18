"""
Utility functions and classes for the AI Textbook backend
"""
from .logging_config import logger
from .exceptions import *
from .error_handlers import add_exception_handlers
from .validators import *

__all__ = [
    "logger",
    "add_exception_handlers",
    # Exceptions
    "TextbookException",
    "ContentNotFoundException", 
    "ValidationError",
    "EmbeddingGenerationError",
    "RAGProcessingError",
    "DatabaseError",
    "ConfigurationError",
    # Validators
    "validate_chapter_slug",
    "validate_content_length",
    "validate_language_code",
    "validate_embedding_vector",
    "validate_textbook_content"
]