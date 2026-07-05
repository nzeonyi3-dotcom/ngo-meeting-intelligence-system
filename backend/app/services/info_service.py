from app.core.config import settings
from app.schemas.info import InfoSchema

class InfoService:
    """Service for application info."""
    
    @staticmethod
    def get_info() -> InfoSchema:
        """Get application info."""
        return InfoSchema(
            name=settings.APP_NAME,
            version=settings.APP_VERSION,
            status="ok"
        )
