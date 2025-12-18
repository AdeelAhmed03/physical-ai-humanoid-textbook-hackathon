from sqlalchemy.orm import Session
from .models import SessionLocal


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()