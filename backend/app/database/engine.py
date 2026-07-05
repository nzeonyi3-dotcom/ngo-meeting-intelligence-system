"""Database engine configuration."""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)

# Log SQL statements in debug mode
if settings.DEBUG:
    @event.listens_for(Engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        logger.debug(f"Executing SQL: {statement}")

def get_engine() -> Engine:
    """Get database engine."""
    return engine
