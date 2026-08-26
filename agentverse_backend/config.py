"""Configuration settings loader using Pydantic Settings."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Base Directory of the AgentVerse workspace
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    GROQ_API_KEY: str = Field(default="")
    MODEL_NAME: str = Field(default="llama-3.3-70b-versatile")
    
    # PostgreSQL Database Configurations
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: str = Field(default="5432")
    DB_NAME: str = Field(default="agentverse")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

try:
    settings = Settings()
    # Validate critical variables early on startup
    if not settings.GROQ_API_KEY:
        from agentverse_backend.utils.logger import logger
        logger.warning("GROQ_API_KEY is not set in environment or .env file. LLM agents will fail to execute.")
except Exception as e:
    from agentverse_backend.utils.logger import logger
    logger.critical(f"Settings initialization failed: {e}")
    raise e
