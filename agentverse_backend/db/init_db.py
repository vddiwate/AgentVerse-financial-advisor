"""Database tables initialization script for PostgreSQL."""

import os
import sys

# Add root directory to sys.path to allow importing from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from agentverse_backend.db.database import engine, Base
# Import models to ensure they register on Base.metadata
from agentverse_backend.db import models
from agentverse_backend.utils.logger import logger

def init_database():
    logger.info("Connecting to PostgreSQL and initializing tables...")
    
    try:
        # Create all registered tables (agent_registry, chat_sessions, chat_messages)
        Base.metadata.create_all(bind=engine)
        logger.success("Tables initialized successfully in PostgreSQL database!")
        logger.info("Created Tables: agent_registry, chat_sessions, chat_messages")
    except Exception as e:
        logger.error(f"DATABASE ERROR: {str(e)}")
        logger.error("Troubleshooting: Verify that PostgreSQL is running, DB exists, and credentials in .env are correct.")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
