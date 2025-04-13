import os
import sys

from django.conf import settings
from loguru import logger


LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# removendo as configurações padrão do loguru
logger.remove()

config = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<blue>{level}</blue> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level> | "
    "<blue>{extra}</blue>"
)

logger.add(sys.stdout, colorize=True, format=config)

log_format = (
    "{time:YYYY-MM-DD HH:mm:ss} | {level} | "
    "{name}:{function}:{line} - {message} | {extra}"
)

logger.add(
    os.path.join(LOG_DIR, "app.log"),
    rotation="10 MB",
    retention="30 days",
    level=settings.LOG_LEVEL,
    format=log_format,
)
