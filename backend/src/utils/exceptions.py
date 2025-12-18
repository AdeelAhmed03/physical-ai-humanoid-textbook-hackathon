from typing import Optional


class TextbookException(Exception):
    """Base exception class for the AI Textbook application"""
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class ContentNotFoundException(TextbookException):
    """Raised when requested content is not found"""
    def __init__(self, content_type: str, identifier: str):
        super().__init__(
            message=f"{content_type} with identifier '{identifier}' not found",
            error_code="CONTENT_NOT_FOUND",
            details={"content_type": content_type, "identifier": identifier}
        )


class ValidationError(TextbookException):
    """Raised when data validation fails"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else {}
        )


class EmbeddingGenerationError(TextbookException):
    """Raised when there's an error generating embeddings"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="EMBEDDING_GENERATION_ERROR",
            details={"original_error": str(original_error)} if original_error else {}
        )


class RAGProcessingError(TextbookException):
    """Raised when there's an error in RAG processing"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="RAG_PROCESSING_ERROR",
            details={"original_error": str(original_error)} if original_error else {}
        )


class DatabaseError(TextbookException):
    """Raised when there's an error with database operations"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details={"original_error": str(original_error)} if original_error else {}
        )


class ConfigurationError(TextbookException):
    """Raised when there's an error with application configuration"""
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details={"config_key": config_key} if config_key else {}
        )