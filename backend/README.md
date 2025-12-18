# AI Textbook Backend

This is the backend API for the AI-Native Textbook with RAG Chatbot project.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For development, also install dev dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
NEON_DATABASE_URL=your-neon-db-url
OPENAI_API_KEY=your-openai-api-key  # Optional
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Running the Application

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Interactive API documentation is available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)