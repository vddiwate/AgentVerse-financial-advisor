"""Agent registry database model representing active specialist agents."""

from sqlalchemy import Column, Integer, String, Boolean, JSON
from agentverse_backend.db.database import Base

class AgentRegistry(Base):
    __tablename__ = "agent_registry"

    agent_id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    tool_names = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, default=True, nullable=False)
