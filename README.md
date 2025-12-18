# AI-Native Textbook with RAG Chatbot

An interactive, AI-powered textbook platform with retrieval-augmented generation (RAG) chatbot functionality, localization support, and personalized learning paths. Developed using Claude Code and Spec-Kit Plus following AI/Spec-Driven Development principles.

## Features

- 📚 Interactive textbook with 6 comprehensive chapters on Physical AI & Humanoid Robotics
- 🤖 RAG-powered chatbot that answers questions based only on textbook content
- 🔍 Semantic search across all textbook content
- 🌐 Multi-language support (English and Urdu)
- 🎯 Personalized learning paths
- 📱 Responsive web interface
- 📝 Content bookmarking and note-taking
- 📊 Progress tracking
- 🌗 Dark/light mode toggle

## Architecture

- **Backend**: FastAPI service with vector database integration
- **Frontend**: Docusaurus-based textbook interface
- **RAG System**: Retrieval-augmented generation for AI responses using OpenAI APIs
- **Database**: Neon Serverless Postgres for relational data
- **Vector Database**: Qdrant for embeddings and semantic search
- **AI Development**: Claude Code for AI-assisted development
- **Spec Management**: Spec-Kit Plus for specification-driven development

## Quick Start

1. **Backend Setup**:
   ```bash
   cd backend/
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend/
   npm install
   npm start
   ```

For detailed instructions, see the [Quickstart Guide](./quickstart.md).

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Docusaurus
- **Database**: Neon Serverless Postgres (relational), Qdrant (vector)
- **AI/ML**: OpenAI APIs, LangChain, Transformers
- **Spec Management**: Spec-Kit Plus
- **AI Development**: Claude Code

## Project Structure

```
ai-textbook/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── db/             # Database models and connections
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── embeddings/     # Embedding utilities
│   └── tests/              # Backend tests
├── frontend/               # Docusaurus frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── pages/          # Page components
│   └── docs/               # Textbook content
├── docs/                   # Project documentation
├── .specify/               # Spec-Kit Plus configuration
└── specs/                  # Project specifications
```

## Documentation

- [API Documentation](./docs/index.md)
- [Quickstart Guide](./quickstart.md)
- [Architecture Specifications](./specs/001-textbook-generation/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.