"""SQLAlchemy database model for tool registry."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from agentverse_backend.db.database import Base

class ToolRegistry(Base):
    __tablename__ = "tool_registry"

    tool_id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Direct Foreign Key connection to AgentRegistry
    agent_id = Column(Integer, ForeignKey("agent_registry.agent_id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationship back to the agent
    agent = relationship("AgentRegistry", back_populates="tools")
