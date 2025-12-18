import logging
from typing import Callable, Awaitable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..utils.exceptions import TextbookException
from ..utils.logging_config import logger


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for the application
    """
    if isinstance(exc, TextbookException):
        # Log the custom exception
        logger.error(f"TextbookException: {exc.error_code} - {exc.message}", extra={
            "error_code": exc.error_code,
            "details": exc.details,
            "url": str(request.url),
            "method": request.method
        })
        
        # Return JSON response with error details
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        )
    elif isinstance(exc, HTTPException):
        # Log the HTTP exception
        logger.error(f"HTTPException: {exc.status_code} - {exc.detail}", extra={
            "status_code": exc.status_code,
            "url": str(request.url),
            "method": request.method
        })
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP_ERROR",
                "message": str(exc.detail)
            }
        )
    else:
        # Log unexpected exceptions
        logger.error(f"Unexpected error: {str(exc)}", extra={
            "url": str(request.url),
            "method": request.method,
            "exception_type": type(exc).__name__
        }, exc_info=True)  # Include traceback for unexpected errors
        
        # Return generic error response
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "An internal error occurred"
            }
        )


def add_exception_handlers(app):
    """
    Add exception handlers to the FastAPI application
    """
    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(TextbookException, exception_handler)
    app.add_exception_handler(HTTPException, exception_handler)