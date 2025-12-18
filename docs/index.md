# AI-Native Textbook Documentation

This documentation provides information about the AI-Native Textbook with RAG Chatbot system.

## Table of Contents
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Search Functionality](#search-functionality)
- [Localization & Personalization](#localization--personalization)
- [Development Setup](#development-setup)

## Architecture

The system is built with a micro-frontend architecture:

- **Backend**: FastAPI-based service handling content management, RAG operations, and user preferences
- **Frontend**: Docusaurus-based textbook interface with integrated chatbot and search functionality

### Key Components

- **Content Service**: Manages textbook chapters and content blocks
- **Embedding Service**: Handles text embedding for RAG operations
- **RAG Service**: Implements retrieval-augmented generation for the chatbot
- **Search Service**: Provides semantic search across textbook content
- **User Service**: Manages user preferences and localization settings

## API Endpoints

### Textbook Endpoints

- `GET /api/textbook/` - Get all textbook chapters with optional language filter
- `GET /api/textbook/{chapter_id}` - Get a specific textbook chapter with optional language filter

### Chat Endpoints

- `POST /api/chat/` - Process user queries using RAG

### Search Endpoints

- `POST /api/search/` - Perform semantic search across textbook content

### Personalization Endpoints

- `POST /api/personalization/settings` - Set user preferences
- `GET /api/personalization/settings/{user_id}` - Get user preferences
- `GET /api/personalization/languages` - Get available languages

## Frontend Components

### Core Components

- **TextbookNavigation**: Navigation sidebar for textbook chapters
- **ChatInterface**: Interactive chat interface with RAG-powered responses
- **SearchBar**: Search functionality to find content across the textbook
- **LanguageSelector**: UI for switching between supported languages
- **PersonalizedPath**: Customizable learning path options

## Search Functionality

The system implements semantic search using embeddings:

1. Content is processed and converted to embeddings during ingestion
2. Queries are converted to embeddings in real-time
3. Similarity search is performed in the vector database
4. Results are returned with context for the RAG system

## Localization & Personalization

The system supports multiple languages and customizable learning experiences:

- Content is available in both English and Urdu
- Users can set language preferences
- Learning paths can be customized based on user needs
- Preferences are stored client-side and can be persisted server-side

## Development Setup

### Backend (Python)

1. Navigate to the backend directory:
   ```
   cd backend/
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```
   uvicorn src.main:app --reload
   ```

### Frontend (Docusaurus)

1. Navigate to the frontend directory:
   ```
   cd frontend/
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```