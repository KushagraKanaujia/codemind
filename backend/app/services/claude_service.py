"""
Claude AI service for code analysis and reasoning.
"""

from typing import List, Dict, Optional
from loguru import logger

from app.core.config import settings


class ClaudeService:
    """Service for interacting with Claude API."""

    def __init__(self):
        """Initialize Claude and OpenAI clients."""
        # Imported here so the keyless demo can run without these SDKs installed.
        from anthropic import Anthropic
        from openai import OpenAI

        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.model = "claude-sonnet-4-5-20250929"

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for text-embedding-3-small)
        """
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")

            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def analyze_code(self, code: str, language: str) -> str:
        """
        Analyze code and provide explanation.

        Args:
            code: Code snippet to analyze
            language: Programming language

        Returns:
            Explanation of what the code does
        """
        try:
            prompt = f"""Analyze this {language} code and explain what it does concisely (2-3 sentences max).
Focus on the main purpose and key functionality.

Code:
```{language}
{code}
```

Provide a clear, technical explanation."""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )

            explanation = message.content[0].text
            logger.info(f"Generated code explanation ({len(explanation)} chars)")
            return explanation

        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            raise

    async def rank_code_results(
        self, results: List[Dict], query: str, criteria: Optional[List[str]] = None
    ) -> tuple[List[Dict], str]:
        """
        Rank code results based on query and criteria using Claude's reasoning.

        Args:
            results: List of code results with basic similarity scores
            query: Original search query
            criteria: Optional ranking criteria (e.g., ['fast', 'readable', 'secure'])

        Returns:
            Tuple of (ranked_results, overall_reasoning)
        """
        try:
            # Build prompt for Claude to rank results
            criteria_str = (
                f"Prioritize: {', '.join(criteria)}" if criteria else "General quality"
            )

            results_text = ""
            for i, result in enumerate(results, 1):
                results_text += f"\n--- Result {i} ---\n"
                results_text += f"Language: {result['language']}\n"
                results_text += f"Source: {result['source']}\n"
                results_text += f"Code:\n{result['code']}\n"

            prompt = f"""You are analyzing code search results for this query: "{query}"

Ranking criteria: {criteria_str}

Here are the search results:
{results_text}

Tasks:
1. Analyze each code snippet
2. Rank them from best to worst for the query
3. For each result, provide:
   - Brief explanation of what it does
   - Why it's ranked at that position
   - Score breakdown if criteria were specified

4. Provide overall reasoning for the rankings

Respond in this JSON format:
{{
    "rankings": [
        {{
            "original_index": 0,
            "rank": 1,
            "explanation": "...",
            "ranking_reason": "...",
            "score_breakdown": {{"fast": 8, "readable": 9}}
        }}
    ],
    "overall_reasoning": "..."
}}"""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            logger.info(f"Generated ranking analysis ({len(response_text)} chars)")

            # Parse JSON response
            import json

            # Extract JSON from response (might be wrapped in markdown)
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            ranking_data = json.loads(json_str)

            # Merge ranking data with original results
            ranked_results = []
            for ranking in ranking_data["rankings"]:
                idx = ranking["original_index"]
                result = results[idx].copy()
                result["rank"] = ranking["rank"]
                result["explanation"] = ranking["explanation"]
                result["ranking_reason"] = ranking["ranking_reason"]
                if "score_breakdown" in ranking:
                    result["score_breakdown"] = ranking["score_breakdown"]
                ranked_results.append(result)

            # Sort by rank
            ranked_results.sort(key=lambda x: x["rank"])

            overall_reasoning = ranking_data.get("overall_reasoning", "")

            return ranked_results, overall_reasoning

        except Exception as e:
            logger.error(f"Error ranking code results: {e}")
            # Fallback: return original order with basic explanations
            logger.warning("Falling back to original order due to ranking error")
            return results, "Ranking failed, showing results by similarity score."
