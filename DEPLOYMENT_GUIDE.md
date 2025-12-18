# Deploying Backend to Railway (Recommended)

This guide will help you deploy your AI Textbook backend to Railway, which is the recommended platform for this application.

## Prerequisites

- A Railway account (free tier available)
- Your repository containing the backend code
- Required environment variables (API keys, database URLs, etc.)

## Deployment Steps

### 1. Create a Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select your repository

### 2. Configure Environment Variables

In your Railway project settings, add the following environment variables:

```
DATABASE_URL=postgresql://username:password@your-db-url:5432/dbname
QDRANT_URL=your-qdrant-instance-url
OPENAI_API_KEY=your_openai_key
JWT_SECRET_KEY=your_secure_jwt_secret
ALLOWED_ORIGINS=https://your-vercel-frontend-url.vercel.app
```

### 3. Railway-Specific Configuration

1. Railway will automatically use the `Dockerfile` in your backend directory
2. The `railway.toml` configuration file specifies the startup command
3. Make sure to use the PORT environment variable (Railway sets this automatically)

## Alternative: Deploying to Hugging Face Spaces

If you prefer Hugging Face Spaces:

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

In your Hugging Face Space settings, add the same environment variables as for Railway.

## Connecting Frontend and Backend

Once your backend is deployed on Railway:

1. Update the `BACKEND_URL` in your Vercel project environment variables
2. The Vercel API proxy in `frontend/api/[[path]].js` will forward requests to your Railway backend
3. The frontend will communicate with the backend through this proxy

## Architecture

```
[User] 
  ↓ (requests to Vercel frontend)
[Vercel Frontend] 
  ↓ (API calls to /api/*)
[Vercel API Proxy] 
  ↓ (forwards to Railway)
[Railway Backend]
```

## Troubleshooting

- Check Railway logs for any startup errors
- Ensure all required environment variables are set
- Verify that the database and vector store are accessible from Railway
- Monitor the resource usage of your deployment

## Notes

- Railway has more generous free tier limitations than many other platforms
- The API proxy approach allows you to hide your backend URL from frontend code
- For production use, Railway offers scalable paid plans