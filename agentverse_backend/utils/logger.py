"""Structured logger utility with daily rotation and 2-day retention."""

import os
import sys
from loguru import logger
from pathlib import Path

# Base log directory
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = LOG_DIR / "agentverse.log"

# Remove the default Loguru handler to prevent duplicate console outputs
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
