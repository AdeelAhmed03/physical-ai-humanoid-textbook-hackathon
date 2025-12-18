# Deployment Runbook

This runbook provides step-by-step instructions for deploying the AI-Native Textbook with RAG Chatbot application.

## Deployment Overview

The AI-Native Textbook application consists of:
- Frontend: Docusaurus-based textbook interface deployed to GitHub Pages
- Backend: FastAPI application deployed to Railway/Render
- Database: Qdrant vector database for embeddings

## Prerequisites

Before deploying, ensure you have:
- Access to GitHub repository with push permissions
- Railway/Render account with appropriate permissions
- Domain name (if using custom domain)
- SSL certificates (if required)
- All required environment variables ready

## Frontend Deployment to GitHub Pages

### Manual Deployment Process
1. **Prepare the environment**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables**:
   - Create/update `.env` file with production API URL:
   ```
   API_BASE_URL=https://your-backend.onrender.com
   ```

3. **Build the application**:
   ```bash
   npm run build
   ```

4. **Deploy using GitHub Actions** (preferred):
   - Push changes to the main branch to trigger the GitHub Actions workflow
   - The workflow will automatically build and deploy to GitHub Pages

### GitHub Actions Deployment
1. **Configure secrets in GitHub repository**:
   - Go to repository Settings > Secrets and variables > Actions
   - Add the following secrets:
     - `API_BASE_URL`: Your production backend URL

2. **Trigger deployment**:
   - Push changes to the `main` branch
   - Or manually trigger the workflow from the Actions tab

3. **Monitor deployment**:
   - Check the Actions tab for workflow status
   - Verify site is accessible after deployment

## Backend Deployment

### Railway Deployment
1. **Install Railway CLI** (if deploying via CLI):
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Link to your project**:
   ```bash
   railway init  # If creating new project
   # OR
   railway link  # If linking to existing project
   ```

4. **Set environment variables**:
   ```bash
   railway variables set QDRANT_URL=your-qdrant-url
   railway variables set QDRANT_API_KEY=your-api-key
   railway variables set EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
   railway variables set SECRET_KEY=your-secret-key
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

### Render Deployment
1. **Connect your repository** to Render via the dashboard
2. **Configure the web service**:
   - Set the root directory to `backend`
   - Use the `render.yaml` configuration file
3. **Set environment variables** in Render dashboard
4. **Enable auto-deploy** from the main branch
5. **Monitor deployment** status in the dashboard

### Manual Docker Deployment
1. **Build the Docker image**:
   ```bash
   cd backend
   docker build -t ai-textbook-backend .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name ai-textbook-backend \
     -p 8000:8000 \
     -e QDRANT_URL=your-qdrant-url \
     -e QDRANT_API_KEY=your-api-key \
     -e SECRET_KEY=your-secret-key \
     ai-textbook-backend
   ```

## Environment Configuration

### Backend Environment Variables
Required variables for production:
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: (If authentication enabled) API key for Qdrant
- `SECRET_KEY`: Secret key for JWT tokens
- `EMBEDDING_MODEL_NAME`: Model name for embeddings

### Frontend Environment Variables
- `API_BASE_URL`: Base URL for the backend API

## Health Checks and Validation

1. **Verify backend health**:
   - Access: `https://your-backend-domain/health/`
   - Expected response: Status 200 with healthy status

2. **Verify readiness**:
   - Access: `https://your-backend-domain/health/ready`
   - Expected response: Status 200 with ready=true

3. **Test API endpoints**:
   - Test textbook content endpoints
   - Test chat functionality
   - Test search functionality

4. **Verify frontend**:
   - Access the GitHub Pages URL
   - Navigate through textbook content
   - Test chat interface
   - Test search functionality

## Post-Deployment Tasks

1. **Monitor logs** for any errors
2. **Verify all metrics** are reporting correctly
3. **Test user workflows** end-to-end
4. **Update DNS records** if needed
5. **Notify stakeholders** of deployment

## Troubleshooting

### Common Issues

1. **Frontend can't connect to backend**:
   - Check `API_BASE_URL` in frontend environment
   - Verify backend is accessible from public internet
   - Check CORS configuration

2. **Backend can't connect to Qdrant**:
   - Verify `QDRANT_URL` and `QDRANT_API_KEY`
   - Check if Qdrant instance is running and accessible
   - Verify network firewall rules

3. **Application is slow**:
   - Check embedding model loading times
   - Verify database connection performance
   - Review resource allocation in deployment platform

4. **Health checks failing**:
   - Check application logs
   - Verify all required services are accessible
   - Review resource utilization

## Rollback Process

If critical issues are found after deployment:

1. **Immediate Actions**:
   - Stop any further automated deployments
   - Inform stakeholders about the issue
   - Activate monitoring and alerting

2. **Execute Rollback**:
   - Follow the rollback procedures in `rollback-procedures.md`
   - For backend: Deploy previous version using Railway/Render
   - For frontend: Revert to previous build if needed

## Monitoring and Maintenance

### Daily Checks
- Verify health check endpoints return healthy status
- Monitor application logs for errors
- Check key metrics and performance indicators

### Weekly Tasks
- Review deployment logs for anomalies
- Verify backup systems are functioning
- Update dependencies as needed

### Monthly Tasks
- Review security logs
- Update environment variables if needed
- Plan for any required maintenance windows