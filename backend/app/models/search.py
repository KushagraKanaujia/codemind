"""
Data models for code search requests and responses.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    """Search query from user."""

    query: str = Field(..., description="Natural language search query", min_length=1)
    criteria: Optional[List[str]] = Field(
        default=None,
        description="Optional criteria for ranking (e.g., 'fast', 'readable', 'secure')",
    )
    max_results: Optional[int] = Field(
        default=5, description="Maximum number of results to return", ge=1, le=10
    )
    language: Optional[str] = Field(
        default=None, description="Optional programming language filter"
    )


class CodeResult(BaseModel):
    """Single code search result."""

    id: str = Field(..., description="Unique identifier")
    code: str = Field(..., description="Code snippet")
    language: str = Field(..., description="Programming language")
    source: str = Field(..., description="Source (repo, file, etc.)")
    similarity_score: float = Field(..., description="Embedding similarity score")
    explanation: Optional[str] = Field(
        default=None, description="Claude's explanation of what this code does"
    )
    score_breakdown: Optional[dict] = Field(
        default=None, description="Scores for each criteria"
    )
    rank: Optional[int] = Field(default=None, description="Ranking position")
    ranking_reason: Optional[str] = Field(
        default=None, description="Why this was ranked at this position"
    )


class SearchResponse(BaseModel):
    """Search response with ranked results."""

    query: str = Field(..., description="Original search query")
    results: List[CodeResult] = Field(..., description="Ranked code results")
    total_found: int = Field(..., description="Total results found before ranking")
    reasoning: Optional[str] = Field(
        default=None, description="Overall reasoning for rankings"
    )
    took_ms: Optional[float] = Field(
        default=None, description="Time taken in milliseconds"
    )


class EmbeddingRequest(BaseModel):
    """Request to generate embeddings."""

    text: str = Field(..., description="Text to embed")


class EmbeddingResponse(BaseModel):
    """Embedding response."""

    embedding: List[float] = Field(..., description="Embedding vector")
    dimensions: int = Field(..., description="Vector dimensions")
