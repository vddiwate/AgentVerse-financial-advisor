"""Agent registry database model representing active specialist agents."""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from agentverse_backend.db.database import Base

class AgentRegistry(Base):
    __tablename__ = "agent_registry"

    agent_id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships: One Agent has one system Prompt, and many Tools
    prompt = relationship("PromptRegistry", back_populates="agent", uselist=False, cascade="all, delete-orphan")
    tools = relationship("ToolRegistry", back_populates="agent", cascade="all, delete-orphan")
