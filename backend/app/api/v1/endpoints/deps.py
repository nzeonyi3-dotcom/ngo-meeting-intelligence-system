"""Dependency injection utilities."""

from sqlalchemy.orm import Session

from app.core.database import get_db


def get_db_session(db: Session = next(get_db())) -> Session:
    """Get database session."""
    return db
