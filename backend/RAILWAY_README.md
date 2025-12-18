# AI Textbook Backend - Railway Deployment

This is the backend service for the AI-Native Textbook with RAG Chatbot, configured for Railway deployment.

## Deployment on Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project" and select "Deploy from GitHub"
3. Choose your repository
4. Railway will automatically detect this as a Python/Docker project

## Environment Variables Required

Add these variables in the Railway dashboard (Settings > Variables):

```
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_instance_url (e.g., http://your-qdrant:6333 or hosted solution)
DATABASE_URL=your_postgresql_database_url
JWT_SECRET_KEY=your_secure_jwt_secret_key
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000
```

## Database Setup

For the PostgreSQL database, you can either:
1. Use Railway's built-in database by connecting via the `DATABASE_URL` variable
2. Use an external PostgreSQL provider

## Qdrant Setup

For the vector database, you have options:
1. Host your own Qdrant instance and provide the URL
2. Use Qdrant Cloud (has free tier)
3. Use alternative vector databases compatible with LangChain

## API Endpoints

After deployment, your backend will expose these endpoints through your Railway URL:
- `/chat/` - RAG-powered chatbot functionality
- `/textbook/` - Textbook content access
- `/search/` - Semantic search across textbook content
- `/personalization/` - Personalized learning path functionality
- `/user/` - User-related operations and data
- `/auth/` - Authentication endpoints

## Connecting to Frontend

Update your frontend's API proxy to use your Railway backend URL:
1. In Vercel project settings, update the `BACKEND_URL` environment variable to your Railway app URL
2. Example: `https://your-railway-app-name.up.railway.app`

## Troubleshooting

- Check Railway logs for any startup errors
- Ensure all required environment variables are set
- Verify that your database and vector store are accessible from Railway
- Monitor resource usage to ensure adequate performance

## Notes

- Railway free tier has sleeping behavior after 5 minutes of inactivity
- For production use, consider upgrading to a paid plan for better performance
- The API proxy approach allows you to hide your backend URL from frontend code