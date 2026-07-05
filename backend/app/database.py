"""Updated database.py for backwards compatibility."""

from app.database import engine, SessionLocal, get_db, Base

__all__ = ["engine", "SessionLocal", "get_db", "Base"]
