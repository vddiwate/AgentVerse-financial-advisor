"""SQLAlchemy database connection engine and session dependency helper."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from agentverse_backend.config import settings

# Create PostgreSQL database engine with connection pool pre-ping to verify connection health
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Session local session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

# Database session context manager / dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
