"""Agent state definitions for LangGraph execution."""

from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    user_id: int           
    messages: List[BaseMessage] 
    session_id: int         
    next_agent: str         
    context: Dict[str, Any] 
