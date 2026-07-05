"""Database session management."""

from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.database.engine import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session() -> Session:
    """Create a new database session."""
    return SessionLocal()
