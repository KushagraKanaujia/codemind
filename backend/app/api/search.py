"""
Search API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from loguru import logger
import time
from typing import List, Optional

from app.models.search import SearchQuery, SearchResponse, CodeResult
from app.services.claude_service import ClaudeService
from app.core.config import settings

router = APIRouter(prefix="/search", tags=["search"])

# Services are created lazily so the API (and the keyless /demo endpoints)
# can start without real API keys.
_claude_service: Optional[ClaudeService] = None


def get_claude_service() -> ClaudeService:
    global _claude_service
    if _claude_service is None:
        if not settings.anthropic_api_key or not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Live search needs ANTHROPIC_API_KEY and OPENAI_API_KEY in backend/.env. "
                "Use /api/v1/demo/search for the keyless demo.",
            )
        _claude_service = ClaudeService()
    return _claude_service


@router.post("/", response_model=SearchResponse)
async def search_code(query: SearchQuery):
    """
    Semantic code search with AI-powered ranking.

    Flow:
    1. Generate embedding for query
    2. Search vector DB for similar code
    3. Claude analyzes and ranks results
    4. Return ranked results with explanations
    """
    start_time = time.time()
    claude_service = get_claude_service()

    try:
        logger.info(f"Search query: '{query.query}' with criteria: {query.criteria}")

        # Step 1: Generate embedding for query
        # Note: You'll need to implement proper embeddings (OpenAI or similar)
        # For MVP, we'll use a placeholder or mock data
        logger.warning("Using mock embeddings - implement OpenAI embeddings for production")
        query_embedding = []  # Placeholder

        # Step 2: Search vector DB
        # For MVP demo without real embeddings, we'll use mock data
        # In production, this would be: vector_service.search_similar(query_embedding, ...)

        # Mock results for testing (remove this once you have real data)
        mock_results = await get_mock_results(query.query, query.language)

        if not mock_results:
            return SearchResponse(
                query=query.query,
                results=[],
                total_found=0,
                reasoning="No results found for this query.",
                took_ms=(time.time() - start_time) * 1000,
            )

        # Step 3: Claude analyzes and ranks results
        logger.info(f"Analyzing {len(mock_results)} results with Claude...")

        ranked_results, overall_reasoning = await claude_service.rank_code_results(
            results=mock_results, query=query.query, criteria=query.criteria
        )

        # Step 4: Convert to response model
        code_results = []
        for result in ranked_results[: query.max_results]:
            code_results.append(
                CodeResult(
                    id=result["id"],
                    code=result["code"],
                    language=result["language"],
                    source=result["source"],
                    similarity_score=result.get("similarity_score", 0.0),
                    explanation=result.get("explanation"),
                    score_breakdown=result.get("score_breakdown"),
                    rank=result.get("rank"),
                    ranking_reason=result.get("ranking_reason"),
                )
            )

        took_ms = (time.time() - start_time) * 1000

        logger.info(
            f"Search completed in {took_ms:.2f}ms, returning {len(code_results)} results"
        )

        return SearchResponse(
            query=query.query,
            results=code_results,
            total_found=len(ranked_results),
            reasoning=overall_reasoning,
            took_ms=took_ms,
        )

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


async def get_mock_results(query: str, language: Optional[str] = None) -> List[dict]:
    """
    Get mock results for testing (remove once you have real vector DB).

    This simulates what the vector search would return.
    """
    # Sample code snippets for different queries
    mock_data = [
        {
            "id": "1",
            "code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
            "language": "python",
            "source": "leetcode/binary_search.py",
            "similarity_score": 0.92,
        },
        {
            "id": "2",
            "code": """function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}""",
            "language": "javascript",
            "source": "algorithms/search.js",
            "similarity_score": 0.89,
        },
        {
            "id": "3",
            "code": """int binary_search(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}""",
            "language": "c",
            "source": "algorithms/search.c",
            "similarity_score": 0.87,
        },
    ]

    # Filter by language if specified
    if language:
        mock_data = [r for r in mock_data if r["language"].lower() == language.lower()]

    return mock_data
