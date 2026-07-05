"""Base model for all database models."""

from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    # Common columns
    created_at = Column(
        DateTime, server_default=func.now(), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        """String representation of model."""
        return f"<{self.__class__.__name__}>"
