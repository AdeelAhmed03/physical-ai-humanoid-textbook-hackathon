import re
from typing import Any
from ..utils.exceptions import ValidationError


def validate_chapter_slug(slug: str) -> bool:
    """
    Validate that a chapter slug follows the required format
    """
    # Check if slug matches the required pattern: lowercase letters, numbers, and hyphens only
    pattern = r'^[a-z0-9-]+$'
    if not re.match(pattern, slug):
        raise ValidationError(
            message=f"Invalid slug format: {slug}. Only lowercase letters, numbers, and hyphens are allowed.",
            field="slug"
        )
    return True


def validate_content_length(content: str, max_length: int = 50000) -> bool:
    """
    Validate that content length is within allowed limits
    """
    if len(content) > max_length:
        raise ValidationError(
            message=f"Content exceeds maximum length of {max_length} characters",
            field="content"
        )
    return True


def validate_language_code(language: str) -> bool:
    """
    Validate that language code is in the supported list
    """
    supported_languages = {"en", "ur"}  # English and Urdu as per requirements
    if language not in supported_languages:
        raise ValidationError(
            message=f"Unsupported language code: {language}. Supported: {', '.join(supported_languages)}",
            field="language"
        )
    return True


def validate_embedding_vector(vector: list, expected_dimension: int) -> bool:
    """
    Validate that an embedding vector has the correct format and dimension
    """
    if not isinstance(vector, list):
        raise ValidationError(
            message="Embedding vector must be a list of floats",
            field="vector"
        )
    
    if len(vector) != expected_dimension:
        raise ValidationError(
            message=f"Embedding vector has incorrect dimension: {len(vector)}. Expected: {expected_dimension}",
            field="vector"
        )
    
    # Check that all values are floats/numbers
    for i, value in enumerate(vector):
        if not isinstance(value, (int, float)):
            raise ValidationError(
                message=f"Embedding vector contains non-numeric value at index {i}: {value}",
                field="vector"
            )
    
    return True


def validate_textbook_content(content: str) -> bool:
    """
    Validate textbook content according to project requirements
    """
    if not content or not content.strip():
        raise ValidationError(
            message="Content cannot be empty",
            field="content"
        )
    
    # Validate content length
    validate_content_length(content)
    
    # Add other content-specific validations here as needed
    
    return True