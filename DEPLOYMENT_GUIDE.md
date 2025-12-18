# Deployment Guide: AI Textbook Project

This guide explains how to deploy the AI Textbook project using the split deployment approach.

## Architecture Overview

The AI Textbook project uses a split deployment architecture:

- **Frontend**: Docusaurus-based textbook interface deployed on Vercel
- **Backend**: FastAPI service deployed separately on Render
- **API Proxy**: Vercel API route that forwards requests from frontend to backend

## Prerequisites

- GitHub account
- Vercel account
- Render account
- Git installed locally

## Deployment Steps

### 1. Backend Deployment (Render)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy backend to Render**:
   - Go to https://dashboard.render.com
   - Click "New +" and select "Web Service"
   - Connect to your GitHub repository
   - Select the `backend` directory
   - Render will automatically detect the `render.yaml` configuration
   - Environment variables will be configured automatically

3. **Note your backend URL**:
   - After deployment completes, note the URL assigned to your backend service
   - It will look like `https://your-service.onrender.com`

### 2. Frontend Deployment (Vercel)

1. **Deploy frontend to Vercel**:
   - Go to https://vercel.com
   - Click "New Project" and import your GitHub repository
   - Select the root directory (not the `frontend` subdirectory)
   - Vercel will automatically detect the `vercel.json` configuration
   - Set the following environment variables in Vercel dashboard:
     - `BACKEND_URL`: The URL of your deployed backend from step 1

2. **Configure Vercel environment variables**:
   - Go to your Vercel project dashboard
   - Navigate to Settings → Environment Variables
   - Add the following variable:
     - Key: `BACKEND_URL`
     - Value: Your backend URL (e.g., `https://ai-textbook-backend.onrender.com`)

### 3. Verification

1. **Test the frontend deployment**:
   - Visit your Vercel URL (e.g., `https://ai-textbook.vercel.app`)
   - Verify that the textbook content loads correctly

2. **Test API functionality**:
   - Test chat, search, and other API-dependent features
   - Check browser developer tools for any API errors

## Configuration Details

### Frontend (Vercel)

- Uses `vercel.json` for deployment configuration
- Serves static Docusaurus content
- Contains API proxy at `/api/[[path]].js` to forward requests to backend
- Environment variable `BACKEND_URL` specifies backend location

### Backend (Render)

- Uses `render.yaml` for deployment configuration
- FastAPI application with proper CORS configuration
- Environment variables configured for security and connectivity
- Database services configured as needed

## Security Considerations

- CORS is configured to only allow requests from your Vercel domain
- API keys and sensitive data are configured as environment variables
- Backend endpoints are protected by proper authentication

## Troubleshooting

### API Requests Failing

1. Verify that `BACKEND_URL` is correctly set in Vercel environment variables
2. Check that the backend service is running and accessible
3. Verify CORS configuration in the backend matches your Vercel domain

### Frontend Build Issues

1. Ensure all dependencies are listed in `frontend/package.json`
2. Check that Docusaurus configuration is correct
3. Verify that API proxy route is properly configured

### Backend Connection Issues

1. Check that the backend is accessible at the configured URL
2. Verify that firewall/VPN is not blocking the connection
3. Confirm that the backend service is running and healthy

## Environment Variables

### Frontend (Vercel)
- `BACKEND_URL`: URL of the deployed backend service

### Backend (Render)
- `QDRANT_URL`: URL of Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant database
- `SECRET_KEY`: Secret key for JWT tokens
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (e.g., `https://ai-textbook.vercel.app,http://localhost:3000`)

## Scaling Considerations

- Frontend scales automatically on Vercel's CDN
- Backend can be scaled by upgrading Render service plans
- Database scaling depends on your Qdrant and Postgres plans