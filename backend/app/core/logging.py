import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings

def setup_logging() -> None:
    """Configure structured JSON logging."""
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    
    # Remove default handlers
    logging.root.handlers = []
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)
    
    # Set specific loggers
    logging.getLogger('uvicorn.access').setLevel(log_level)
    logging.getLogger('uvicorn.error').setLevel(log_level)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
