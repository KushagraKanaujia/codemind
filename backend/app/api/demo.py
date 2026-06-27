"""
Demo API endpoints - Works without real API keys.
Returns realistic mock data to demonstrate CodeMind functionality.
"""

from fastapi import APIRouter
from app.models.search import SearchQuery, SearchResponse, CodeResult

router = APIRouter(prefix="/demo", tags=["demo"])


# Mock search results database
DEMO_RESULTS = {
    "binary search": [
        {
            "id": "demo-1",
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
            "source": "algorithms/binary_search.py",
            "similarity_score": 0.95,
            "explanation": "This is a classic iterative binary search implementation. It uses two pointers (left and right) to repeatedly halve the search space, making it very efficient with O(log n) time complexity. The code is clean, readable, and handles edge cases well.",
            "rank": 1,
            "ranking_reason": "Ranks #1 because it's the most Pythonic implementation with clear variable names, efficient O(log n) performance, and easy-to-understand logic. Perfect balance of readability and performance.",
            "score_breakdown": {"fast": 9, "readable": 10, "simple": 9}
        },
        {
            "id": "demo-2",
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
            "source": "algorithms/binary_search.js",
            "similarity_score": 0.92,
            "explanation": "JavaScript implementation using modern ES6+ syntax with const and let. Also uses the two-pointer approach with O(log n) complexity. The Math.floor ensures integer division for the midpoint calculation.",
            "rank": 2,
            "ranking_reason": "Ranks #2 because while it's performant and clear, it uses slightly more verbose syntax compared to Python. Still excellent for JavaScript environments.",
            "score_breakdown": {"fast": 9, "readable": 8, "simple": 8}
        },
        {
            "id": "demo-3",
            "code": """int binarySearch(int arr[], int n, int target) {
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
            "source": "algorithms/binary_search.c",
            "similarity_score": 0.89,
            "explanation": "C implementation with manual array length parameter. Uses a clever overflow-safe midpoint calculation: left + (right - left) / 2 instead of (left + right) / 2, which prevents integer overflow for large indices.",
            "rank": 3,
            "ranking_reason": "Ranks #3 because it's the most performance-optimized with overflow protection, but requires more boilerplate (array length parameter) and is less readable than higher-level languages.",
            "score_breakdown": {"fast": 10, "readable": 6, "simple": 6}
        }
    ],
    "sorting": [
        {
            "id": "demo-4",
            "code": """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)""",
            "language": "python",
            "source": "algorithms/quicksort.py",
            "similarity_score": 0.94,
            "explanation": "Elegant quicksort using Python list comprehensions. Very readable and concise, though uses extra memory for the sublists. O(n log n) average case, O(n²) worst case.",
            "rank": 1,
            "ranking_reason": "Ranks #1 for its exceptional readability and Pythonic style. While not the most memory-efficient, it's perfect for understanding the algorithm and works well for most practical cases.",
            "score_breakdown": {"fast": 8, "readable": 10, "simple": 9}
        },
        {
            "id": "demo-5",
            "code": """function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    return merge(left, right);
}

function merge(left, right) {
    const result = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
        if (left[i] < right[j]) result.push(left[i++]);
        else result.push(right[j++]);
    }
    return result.concat(left.slice(i)).concat(right.slice(j));
}""",
            "language": "javascript",
            "source": "algorithms/merge_sort.js",
            "similarity_score": 0.91,
            "explanation": "Stable merge sort implementation with guaranteed O(n log n) time complexity. More predictable than quicksort but uses extra O(n) space for merging.",
            "rank": 2,
            "ranking_reason": "Ranks #2 because it offers better worst-case guarantees than quicksort (always O(n log n)), but is slightly more complex and uses more memory. Great when stability matters.",
            "score_breakdown": {"fast": 9, "readable": 8, "simple": 7}
        }
    ],
    "default": [
        {
            "id": "demo-default",
            "code": """# Example code snippet
def example_function(param):
    \"\"\"This is a demo result.\"\"\"
    return f"Processed: {param}\"""",
            "language": "python",
            "source": "demo/example.py",
            "similarity_score": 0.75,
            "explanation": "This is a demo result. In the real app with API keys, Claude would analyze actual code from the database and provide detailed explanations.",
            "rank": 1,
            "ranking_reason": "Demo mode active - get API keys to see real results!",
            "score_breakdown": {"fast": 7, "readable": 8, "simple": 8}
        }
    ]
}


def find_best_match(query: str):
    """Find the best matching demo results for a query."""
    query_lower = query.lower()

    # Check for keyword matches
    if "binary" in query_lower or "search" in query_lower:
        return DEMO_RESULTS["binary search"]
    elif "sort" in query_lower:
        return DEMO_RESULTS["sorting"]
    else:
        return DEMO_RESULTS["default"]


@router.post("/search", response_model=SearchResponse)
async def demo_search(query: SearchQuery):
    """
    Demo search endpoint - no API keys required!

    Returns realistic mock results to demonstrate CodeMind's features.
    """

    # Find matching demo results
    results = find_best_match(query.query)

    # Convert to CodeResult objects
    code_results = []
    for result in results[:query.max_results]:
        code_results.append(
            CodeResult(
                id=result["id"],
                code=result["code"],
                language=result["language"],
                source=result["source"],
                similarity_score=result["similarity_score"],
                explanation=result.get("explanation"),
                score_breakdown=result.get("score_breakdown"),
                rank=result.get("rank"),
                ranking_reason=result.get("ranking_reason"),
            )
        )

    reasoning = """I analyzed these code implementations and ranked them based on your criteria.

In production mode (with API keys), I would:
1. Generate embeddings for your query
2. Search through all 203 code examples in the vector database
3. Analyze each result in detail
4. Rank them based on your specific criteria
5. Provide detailed reasoning for each ranking

This is DEMO MODE - showing you what the interface looks like with sample data."""

    return SearchResponse(
        query=query.query,
        results=code_results,
        total_found=len(results),
        reasoning=reasoning,
        took_ms=125.5  # Simulated response time
    )


@router.get("/info")
async def demo_info():
    """Information about demo mode."""
    return {
        "mode": "demo",
        "message": "Running in demo mode - no API keys required!",
        "features": [
            "✅ Full UI functionality",
            "✅ Realistic mock search results",
            "✅ Simulated Claude reasoning",
            "⏸️  Real API calls (need keys)",
            "⏸️  Real vector database search (need Supabase)",
            "⏸️  203 code examples (need to index)"
        ],
        "try_queries": [
            "binary search",
            "sorting algorithm",
            "anything else (will show generic demo)"
        ],
        "next_steps": [
            "1. Get Anthropic API key: https://console.anthropic.com",
            "2. Get OpenAI API key: https://platform.openai.com",
            "3. Set up Supabase: See docs/SUPABASE_SETUP.md",
            "4. Switch to production mode"
        ]
    }
