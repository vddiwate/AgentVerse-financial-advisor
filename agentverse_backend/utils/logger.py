"""Structured logger utility with daily rotation, 2-day retention, and standard logging interception."""

import os
import sys
import logging
from loguru import logger
from pathlib import Path

# Base log directory
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = LOG_DIR / "agentverse.log"

# Remove default Loguru handler to prevent duplicates
logger.remove()

# Add styled colored console logger
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Add file logger with daily midnight rotation, 2-day retention, and thread-safe queueing
logger.add(
    str(LOG_FILE),
    rotation="00:00",
    retention="2 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    encoding="utf-8",
    enqueue=True
)

class InterceptHandler(logging.Handler):
    """Handler to intercept standard library logging messages and forward them to Loguru."""

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# Configure standard root logging to route all messages to Loguru interceptor handler
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
