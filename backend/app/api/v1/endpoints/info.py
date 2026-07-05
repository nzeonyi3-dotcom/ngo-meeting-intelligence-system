from fastapi import APIRouter, Depends
from app.schemas.info import InfoSchema, HealthSchema
from app.services.info_service import InfoService

router = APIRouter(prefix="/api/v1", tags=["info"])

@router.get("/info", response_model=InfoSchema)
async def get_info() -> InfoSchema:
    """Get application information."""
    return InfoService.get_info()

@router.get("/health", response_model=HealthSchema)
async def health_check() -> HealthSchema:
    """Health check endpoint."""
    return HealthSchema(status="ok")
