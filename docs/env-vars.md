# Environment Variables

This document lists all environment variables required for the AI-Native Textbook with RAG Chatbot application.

## Backend Environment Variables

### Required Variables
- `QDRANT_URL`: URL for the Qdrant vector database (e.g., `http://localhost:6333` or hosted URL)
- `EMBEDDING_MODEL_NAME`: Name of the sentence transformer model to use (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `QDRANT_API_KEY`: (Optional) API key for Qdrant if authentication is enabled

### Optional Variables
- `PORT`: Port number for the backend server (default: `8000`)
- `HOST`: Host address for the backend server (default: `0.0.0.0`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `MAX_CONTENT_LENGTH`: Maximum length for content chunks (default: `1000`)
- `EMBEDDING_DIMENSION`: Dimension of the embedding vectors (default: `384`)

### Security Variables
- `SECRET_KEY`: Secret key for signing JWT tokens (required for auth if implemented)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: `30`)

## Frontend Environment Variables

### API Configuration
- `API_BASE_URL`: Base URL for the backend API (e.g., `https://your-backend.onrender.com`)

### Optional Variables
- `GA_MEASUREMENT_ID`: Google Analytics measurement ID (if using analytics)
- `SENTRY_DSN`: Sentry DSN for error tracking (if using Sentry)

## Development vs Production

### Development
For local development, use the `.env` file in the backend directory with appropriate values for your local setup.

### Staging
For staging environments, use the same variables but with staging-specific values (e.g., staging database URL).

### Production
For production environments, ensure all sensitive variables (API keys, database URLs) are properly secured and managed through the deployment platform's secrets management.

## Setting Environment Variables

### Local Development
Copy `.env.example` to `.env` and set appropriate values:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your values
```

### Railway Deployment
Set environment variables through the Railway dashboard or CLI:
```bash
railway config set QDRANT_URL=your-qdrant-url
```

### Render Deployment
Set environment variables through the Render dashboard:
1. Go to your service settings
2. Navigate to "Environment" section
3. Add your key-value pairs

### GitHub Actions
Set environment variables in the repository settings under Secrets and Variables.

## Required Services

The application requires the following external services:
- Qdrant vector database for embedding storage and similarity search
- (Optional) OpenAI API or other LLM provider for enhanced RAG functionality