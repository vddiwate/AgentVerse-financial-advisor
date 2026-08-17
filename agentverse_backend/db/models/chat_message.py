"""Chat message database model representing individual messages in a session."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from agentverse_backend.db.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)  # "user", "assistant", "system"
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Establish relationship back to session
    session = relationship("ChatSession", back_populates="messages")
