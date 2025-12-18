from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from .utils.error_handlers import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Import configuration
from .config import settings

# Import routers
from .api.chat_router import router as chat_router
from .api.textbook_router import router as textbook_router
from .api.search_router import router as search_router
from .api.personalization_router import router as personalization_router
from .api.health import router as health_router
from .api.user_router import router as user_router
from .api.auth_router import router as auth_router
from .api.better_auth_router import router as better_auth_router

# Import database models and create tables
from .db.models import create_tables

# Create database tables on startup
create_tables()

app = FastAPI(title="AI Textbook Backend", version="1.0.0")

# Add CORS middleware for security
# Allow origins from environment variable, default to wildcard for development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(chat_router)
app.include_router(textbook_router)
app.include_router(search_router)
app.include_router(personalization_router)
app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(better_auth_router)

@app.get("/")
def read_root():
    return {"message": "AI Textbook Backend API"}