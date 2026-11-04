
from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class Source(BaseModel):
    doc_id: str
    title: str
    chunk_index: int
    score: float
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = Field(default_factory=list)
    session_id: Optional[str] = None
