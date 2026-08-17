"""Chat session database model grouping conversation turns under session context."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from agentverse_backend.db.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Establish relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
