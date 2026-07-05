"""Updated info endpoints with single health check."""

from fastapi import APIRouter
from app.schemas.info import InfoSchema, HealthSchema
from app.services.info_service import InfoService

router = APIRouter(prefix="/api/v1", tags=["system"])

@router.get(
    "/info",
    response_model=InfoSchema,
    summary="Get application information",
    description="Returns application name, version, and status",
)
async def get_info() -> InfoSchema:
    """Get application information including name, version, and status."""
    return InfoService.get_info()

@router.get(
    "/health",
    response_model=HealthSchema,
    summary="Health check",
    description="Returns application health status",
)
async def health_check() -> HealthSchema:
    """Health check endpoint for monitoring and container orchestration.
    
    Returns:
        HealthSchema: Health status of the application
    """
    return HealthSchema(status="ok")
