import logging
import sys
from datetime import datetime
from pathlib import Path

from core.config import settings


def setup_logging():
    """Setup application logging configuration."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else 'INFO'),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log")
        ]
    )
    
    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logging.getLogger(__name__)


def get_logger(name: str):
    """Get logger instance for a specific module"""
    return logging.getLogger(name)
