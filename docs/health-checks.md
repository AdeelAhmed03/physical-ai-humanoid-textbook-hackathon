# Health Checks

This document explains the health check endpoints available in the AI-Native Textbook backend.

## Available Endpoints

### 1. Basic Health Check
- **Endpoint**: `GET /health/`
- **Purpose**: Provides a general health status of the application
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2023-10-01T10:00:00.000Z",
    "uptime": 3600.5,
    "version": "1.0.0",
    "services": {
      "vector_db": "ok"
    }
  }
  ```

### 2. Readiness Check
- **Endpoint**: `GET /health/ready`
- **Purpose**: Indicates if the application is ready to accept traffic
- **Use Case**: For load balancers and orchestration platforms to determine if the service can handle requests
- **Response**:
  ```json
  {
    "ready": true,
    "message": "Application is ready",
    "checks": {
      "vector_db": true,
      "embedding_service": true
    }
  }
  ```

### 3. Liveness Check
- **Endpoint**: `GET /health/live`
- **Purpose**: Indicates if the application is alive and responding
- **Use Case**: For orchestration platforms to determine if the service needs to be restarted
- **Response**:
  ```json
  {
    "alive": true,
    "message": "Application is alive"
  }
  ```

### 4. Detailed Health Check
- **Endpoint**: `GET /health/detailed`
- **Purpose**: Provides detailed system and application metrics
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2023-10-01T10:00:00.000Z",
    "uptime": 3600.5,
    "version": "1.0.0",
    "system": {
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "disk_usage_percent": 60.1,
      "process_count": 10
    },
    "app": {
      "name": "AI Textbook Backend",
      "host": "0.0.0.0",
      "port": 8000,
      "log_level": "INFO"
    }
  }
  ```

## Implementation Details

The health checks verify:
- Connectivity to the Qdrant vector database
- Availability of the embedding service
- Basic application responsiveness
- System resource utilization

## Integration with Deployment Platforms

### Railway
Configure health checks in `.railway.yml` to use the `/health/ready` endpoint for readiness probes.

### Render
Set the health check path in `render.yaml` to use `/health/` as the health check endpoint.

### Kubernetes (if applicable)
- Use `/health/live` for liveness probes
- Use `/health/ready` for readiness probes