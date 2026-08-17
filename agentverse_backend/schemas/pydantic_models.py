"""Pydantic validation models for chat request and response schemas."""

from pydantic import BaseModel
from typing import Optional, List

class ChatQueryRequest(BaseModel):
    user_id: int
    query: str
    session_id: Optional[int] = None  # None indicates a request to create a new session

class ChatQueryResponse(BaseModel):
    response_text: str
    chart_data: Optional[dict] = None
    sources: Optional[List[str]] = None
    session_id: int
