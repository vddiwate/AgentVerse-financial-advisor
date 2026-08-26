"""SQLAlchemy database model for prompt registry."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from agentverse_backend.db.database import Base

class PromptRegistry(Base):
    __tablename__ = "prompt_registry"

    prompt_id = Column(Integer, primary_key=True, index=True)
    prompt_name = Column(String, unique=True, index=True, nullable=False)
    prompt_text = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Direct Foreign Key connection to AgentRegistry (unique=True enforces One-to-One)
    agent_id = Column(Integer, ForeignKey("agent_registry.agent_id", ondelete="SET NULL"), unique=True, nullable=True, index=True)

    # Relationship back to the agent
    agent = relationship("AgentRegistry", back_populates="prompt")
