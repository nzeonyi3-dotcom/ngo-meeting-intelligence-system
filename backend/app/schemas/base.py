"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema with common fields."""

    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
