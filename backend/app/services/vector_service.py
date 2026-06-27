"""
Vector database service using Supabase pgvector.
"""

from typing import List, Dict, Optional
from supabase import create_client, Client
from loguru import logger

from app.core.config import settings


class VectorService:
    """Service for vector similarity search using Supabase pgvector."""

    def __init__(self):
        """Initialize Supabase client."""
        self.client: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )
        self.table_name = "code_embeddings"

    async def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 10,
        language: Optional[str] = None,
    ) -> List[Dict]:
        """
        Search for similar code using vector similarity.

        Args:
            query_embedding: Query vector
            limit: Maximum number of results
            language: Optional language filter

        Returns:
            List of similar code results
        """
        try:
            # Build query
            query = self.client.table(self.table_name).select("*")

            # Add language filter if specified
            if language:
                query = query.eq("language", language)

            # Note: For pgvector similarity search, you'll need to use RPC functions
            # This is a simplified version - you'll need to create a custom function in Supabase

            # For now, placeholder that returns all results
            # In production, use: .rpc('match_code_embeddings', {'query_embedding': query_embedding, 'match_threshold': 0.7, 'match_count': limit})

            response = query.limit(limit).execute()

            results = response.data
            logger.info(f"Found {len(results)} similar code snippets")

            return results

        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise

    async def insert_code_embedding(
        self,
        code: str,
        embedding: List[float],
        language: str,
        source: str,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Insert code with embedding into vector database.

        Args:
            code: Code snippet
            embedding: Embedding vector
            language: Programming language
            source: Source information
            metadata: Additional metadata

        Returns:
            ID of inserted record
        """
        try:
            data = {
                "code": code,
                "embedding": embedding,
                "language": language,
                "source": source,
                "metadata": metadata or {},
            }

            response = self.client.table(self.table_name).insert(data).execute()

            record_id = response.data[0]["id"]
            logger.info(f"Inserted code embedding with ID: {record_id}")

            return record_id

        except Exception as e:
            logger.error(f"Error inserting code embedding: {e}")
            raise

    async def batch_insert(self, code_items: List[Dict]) -> List[str]:
        """
        Batch insert multiple code embeddings.

        Args:
            code_items: List of dicts with keys: code, embedding, language, source, metadata

        Returns:
            List of inserted IDs
        """
        try:
            response = self.client.table(self.table_name).insert(code_items).execute()

            ids = [item["id"] for item in response.data]
            logger.info(f"Batch inserted {len(ids)} code embeddings")

            return ids

        except Exception as e:
            logger.error(f"Error batch inserting embeddings: {e}")
            raise

    async def delete_embedding(self, embedding_id: str) -> bool:
        """Delete an embedding by ID."""
        try:
            self.client.table(self.table_name).delete().eq("id", embedding_id).execute()
            logger.info(f"Deleted embedding: {embedding_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting embedding: {e}")
            return False
