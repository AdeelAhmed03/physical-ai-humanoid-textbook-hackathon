# AI Textbook Backend

This is the backend service for the AI-Native Textbook with RAG Chatbot. It provides API endpoints for textbook content, chat functionality, search, personalization, and user management.

## Deployment Options

This backend can be deployed to:
- **Railway** (recommended) - See RAILWAY_README.md for detailed instructions
- **Hugging Face Spaces** - See DEPLOYMENT_HF_GUIDE.md for instructions
- **Render** - Supports Python web services
- **Other cloud platforms** - Using the provided Dockerfile

## API Endpoints

- `/chat/` - RAG-powered chatbot functionality
- `/textbook/` - Textbook content access
- `/search/` - Semantic search across textbook content
- `/personalization/` - Personalized learning path functionality
- `/user/` - User-related operations and data
- `/auth/` - Authentication endpoints

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `QDRANT_URL` - Vector database connection string
- `OPENAI_API_KEY` - OpenAI API key for embeddings and completions
- `JWT_SECRET_KEY` - Secret key for JWT token signing
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins (default: "*")