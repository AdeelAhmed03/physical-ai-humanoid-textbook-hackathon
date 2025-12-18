from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time
import asyncio
from datetime import datetime

from ..config import settings

router = APIRouter(prefix="/health", tags=["health"])


class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    uptime: float
    version: str
    services: Dict[str, str]


class ReadyStatus(BaseModel):
    ready: bool
    message: str
    checks: Dict[str, bool]


class LiveStatus(BaseModel):
    alive: bool
    message: str


# Store application start time
start_time = time.time()
app_version = "1.0.0"


@router.get("/", response_model=HealthStatus)
async def health_check():
    """
    General health check endpoint
    """
    # In a real implementation, you would check the status of your services
    # like database connections, external APIs, etc.
    
    services_status = {}
    
    # Check if Qdrant is accessible (mock implementation)
    try:
        # This would be replaced with actual Qdrant connection check
        services_status["vector_db"] = "ok"
    except Exception:
        services_status["vector_db"] = "error"
    
    # Calculate overall status
    overall_status = "healthy" if all(status == "ok" for status in services_status.values()) else "unhealthy"
    
    return HealthStatus(
        status=overall_status,
        timestamp=datetime.utcnow(),
        uptime=time.time() - start_time,
        version=app_version,
        services=services_status
    )


@router.get("/ready", response_model=ReadyStatus)
async def readiness_check():
    """
    Readiness check - indicates if the application is ready to accept traffic
    """
    readiness_checks = {}
    
    # Check if all required services are available
    try:
        # Check Qdrant connection
        # This would be replaced with actual connection verification
        readiness_checks["vector_db"] = True
    except Exception:
        readiness_checks["vector_db"] = False
    
    # Check if embedding service is ready
    try:
        # This would be replaced with actual embedding service check
        readiness_checks["embedding_service"] = True
    except Exception:
        readiness_checks["embedding_service"] = False
    
    # Overall readiness
    ready = all(readiness_checks.values())
    message = "Application is ready" if ready else "One or more services are not ready"
    
    return ReadyStatus(
        ready=ready,
        message=message,
        checks=readiness_checks
    )


@router.get("/live", response_model=LiveStatus)
async def liveness_check():
    """
    Liveness check - indicates if the application is alive and responding
    """
    # Basic liveness check - if we can respond to this request, we're alive
    return LiveStatus(
        alive=True,
        message="Application is alive"
    )


@router.get("/detailed")
async def detailed_health():
    """
    Detailed health information
    """
    import psutil
    import os
    
    # System metrics
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "uptime": time.time() - start_time,
        "version": app_version,
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "disk_usage_percent": disk_usage,
            "process_count": len(psutil.pids())
        },
        "app": {
            "name": "AI Textbook Backend",
            "host": settings.host,
            "port": settings.port,
            "log_level": settings.log_level
        }
    }