"""
Script to index code examples into Supabase vector database.

Usage:
    python scripts/index_code_data.py --data-file ../data/sample_code.json
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.claude_service import ClaudeService
from app.services.vector_service import VectorService
from loguru import logger


async def load_code_data(file_path: str) -> List[Dict]:
    """Load code examples from JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} code examples from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def prepare_text_for_embedding(code: str, language: str, description: str = "") -> str:
    """Prepare code for embedding with context."""
    text = f"""Language: {language}
{description if description else ''}

Code:
{code}"""
    return text.strip()


async def index_code_examples(data_file: str):
    """Index code examples with embeddings."""
    logger.info("Starting code indexing process...")

    # Initialize services
    claude_service = ClaudeService()
    vector_service = VectorService()

    # Load data
    code_examples = await load_code_data(data_file)

    # Process each example
    indexed_count = 0
    failed_count = 0

    for i, example in enumerate(code_examples, 1):
        try:
            logger.info(f"Processing {i}/{len(code_examples)}: {example['source']}")

            # Prepare text for embedding
            text = prepare_text_for_embedding(
                code=example['code'],
                language=example['language'],
                description=example.get('description', '')
            )

            # Generate embedding
            logger.info("  Generating embedding...")
            embedding = await claude_service.generate_embedding(text)

            # Check if embedding is valid
            if not embedding or len(embedding) == 0:
                logger.warning(f"  Skipping {example['source']} - no embedding generated")
                logger.warning("  Make sure you've set up OpenAI API key (see docs/EMBEDDINGS.md)")
                continue

            # Insert into database
            logger.info("  Inserting into database...")
            record_id = await vector_service.insert_code_embedding(
                code=example['code'],
                embedding=embedding,
                language=example['language'],
                source=example['source'],
                metadata={
                    'description': example.get('description', ''),
                    'tags': example.get('tags', [])
                }
            )

            logger.info(f"  ✓ Indexed successfully (ID: {record_id})")
            indexed_count += 1

        except Exception as e:
            logger.error(f"  ✗ Failed to index {example.get('source', 'unknown')}: {e}")
            failed_count += 1

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Indexing Complete!")
    logger.info(f"  Successfully indexed: {indexed_count}")
    logger.info(f"  Failed: {failed_count}")
    logger.info(f"  Total: {len(code_examples)}")
    logger.info("=" * 50)


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Index code examples into vector database')
    parser.add_argument(
        '--data-file',
        type=str,
        default='../data/sample_code.json',
        help='Path to JSON file with code examples'
    )

    args = parser.parse_args()

    # Check if file exists
    data_path = Path(args.data_file)
    if not data_path.exists():
        logger.error(f"Data file not found: {args.data_file}")
        logger.info("Please provide a valid path to code examples JSON file")
        sys.exit(1)

    # Run indexing
    await index_code_examples(str(data_path))


if __name__ == '__main__':
    asyncio.run(main())
