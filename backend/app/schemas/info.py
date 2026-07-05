from pydantic import BaseModel

class InfoSchema(BaseModel):
    """Application info schema."""
    name: str
    version: str
    status: str

class HealthSchema(BaseModel):
    """Health check schema."""
    status: str
