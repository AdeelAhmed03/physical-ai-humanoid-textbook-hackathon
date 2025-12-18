# Deploying Backend to Hugging Face Spaces

This guide will help you deploy your AI Textbook backend to Hugging Face Spaces.

## Prerequisites

- A Hugging Face account
- Your repository containing the backend code
- Required environment variables (API keys, database URLs, etc.)

## Deployment Steps

### 1. Create a Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - Name: Your preferred space name
   - License: MIT (or your preferred license)
   - SDK: Docker (recommended for full control)
   - Hardware: Choose based on your needs (CPU for basic usage)
   - Existing repo: Point to your GitHub repository

### 2. Configure Environment Variables

In your Hugging Face Space settings, add the following environment variables:

```
DATABASE_URL=postgresql://username:password@your-db-url:5432/dbname
QDRANT_URL=your-qdrant-instance-url
OPENAI_API_KEY=your_openai_key
JWT_SECRET_KEY=your_secure_jwt_secret
ALLOWED_ORIGINS=https://your-vercel-frontend-url.vercel.app
```

### 3. Prepare Your Repository

Make sure your repository contains:
- `app.py` (entry point for the application)
- `Dockerfile` (container configuration)
- `requirements.txt` (Python dependencies)
- `.env.example` (example environment variables)

### 4. Alternative: Gradio Space

If you prefer to use Gradio as the SDK instead of Docker:

1. Create a `app.py` file in the root directory with:
```python
from your_app import app  # Import your FastAPI app

# This allows Hugging Face to run your app
import uvicorn
from threading import Thread
import time
import requests

# Start FastAPI in a separate thread
def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# Start the server
thread = Thread(target=start_fastapi, daemon=True)
thread.start()

# Wait a bit for the server to start
time.sleep(3)

# Now the app is running and Hugging Face can access it
```

2. Use the Gradio SDK when creating the Space

## Connecting Frontend and Backend

Once your backend is deployed on Hugging Face:

1. Update the `BACKEND_URL` in your Vercel project environment variables
2. The Vercel API proxy in `frontend/api/[[path]].js` will forward requests to your Hugging Face backend
3. The frontend will communicate with the backend through this proxy

## Architecture

```
[User] 
  ↓ (requests to Vercel frontend)
[Vercel Frontend] 
  ↓ (API calls to /api/*)
[Vercel API Proxy] 
  ↓ (forwards to Hugging Face)
[Hugging Face Backend]
```

## Troubleshooting

- Check Hugging Face Space logs for any startup errors
- Ensure all required environment variables are set
- Verify that the database and vector store are accessible from the Hugging Face environment
- Monitor the resource usage of your Space

## Notes

- Hugging Face Spaces have rate limits and resource constraints
- For production use, consider using Hugging Face Inference Endpoints or deploying to a dedicated cloud provider
- The API proxy approach allows you to hide your backend URL from frontend code