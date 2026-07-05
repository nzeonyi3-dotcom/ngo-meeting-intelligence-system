"""Database configuration and session management."""

# This module is kept for backwards compatibility
# All database functionality has been moved to app/database/ package

from app.database import engine, SessionLocal, get_db, Base

__all__ = ["engine", "SessionLocal", "get_db", "Base"]
