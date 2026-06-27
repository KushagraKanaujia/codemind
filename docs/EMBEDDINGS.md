# Embeddings Setup Guide

CodeMind uses embeddings for semantic code search. Since Anthropic doesn't provide an embeddings API yet, we'll use OpenAI's embeddings.

## Why OpenAI Embeddings?

- **Cost-effective**: $0.02 per 1M tokens
- **High quality**: `text-embedding-3-small` is fast and accurate
- **Well-documented**: Easy to integrate
- **Industry standard**: Used by most semantic search apps

## Step 1: Get OpenAI API Key

1. Go to [https://platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to **API Keys** section
4. Click "Create new secret key"
5. Name it: `codemind-embeddings`
6. Copy the key (starts with `sk-...`)
7. Add to `backend/.env`:

```bash
OPENAI_API_KEY=sk-your-key-here
```

## Step 2: Install OpenAI Python SDK

Already included in `requirements.txt`, but if needed:

```bash
pip install openai
```

## Step 3: Update Claude Service

Replace the placeholder in `backend/app/services/claude_service.py`:

```python
from openai import OpenAI

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.model = "claude-sonnet-4-5-20250929"

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
```

## Step 4: Update Config

Add OpenAI key to `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    # ... existing fields ...

    # OpenAI (for embeddings)
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
```

## Step 5: Update Requirements

Add to `backend/requirements.txt` if not already there:

```
openai==1.6.1
```

## Step 6: Update Search API

In `backend/app/api/search.py`, replace the mock embedding call:

```python
@router.post("/", response_model=SearchResponse)
async def search_code(query: SearchQuery):
    # ...

    # Generate embedding for query
    query_embedding = await claude_service.generate_embedding(query.query)

    # Search vector DB with real embedding
    results = await vector_service.search_similar(
        query_embedding=query_embedding,
        limit=query.max_results * 2,  # Get more for Claude to rank
        language=query.language
    )

    # ... rest of the function
```

## Embedding Best Practices

### 1. Batch Processing
When indexing many code snippets, batch them:

```python
async def batch_embed(texts: List[str], batch_size: int = 100):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = openai_client.embeddings.create(
            input=batch,
            model="text-embedding-3-small"
        )
        embeddings.extend([data.embedding for data in response.data])
    return embeddings
```

### 2. Add Context to Code
Better embeddings by adding context:

```python
def prepare_text_for_embedding(code: str, language: str, description: str = ""):
    """Prepare code for embedding with context."""
    text = f"""
Language: {language}
{description if description else ''}

Code:
{code}
"""
    return text.strip()
```

### 3. Cache Embeddings
Never regenerate embeddings for the same text:

```python
import hashlib
import json

def get_embedding_cache_key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# Store in Redis:
# redis.set(f"embedding:{cache_key}", json.dumps(embedding))
```

## Cost Estimation

**text-embedding-3-small** pricing: $0.02 / 1M tokens

Example costs:
- 1,000 code snippets (avg 100 tokens each) = 100k tokens = **$0.002**
- 10,000 code snippets = 1M tokens = **$0.02**
- 100,000 code snippets = 10M tokens = **$0.20**

For MVP with 1,000 examples: **less than 1 cent** ✅

## Alternative: Sentence Transformers (Free)

If you want to avoid OpenAI costs, use sentence-transformers:

```bash
pip install sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    embedding = model.encode(text)
    return embedding.tolist()
```

**Pros:**
- Free, runs locally
- No API calls, no rate limits

**Cons:**
- Slower (CPU-based unless you have GPU)
- Lower quality than OpenAI
- Needs 512MB+ RAM

## Troubleshooting

### Error: "No API key provided"
- Check your `.env` file has `OPENAI_API_KEY`
- Verify the key starts with `sk-`
- Restart the backend after adding the key

### Rate limit errors
- OpenAI has rate limits (3,000 RPM on free tier)
- Use batch processing
- Add retry logic with exponential backoff

### Wrong embedding dimensions
- `text-embedding-3-small` = 1536 dimensions
- Make sure your Supabase table uses `vector(1536)`
- If using sentence-transformers: `all-MiniLM-L6-v2` = 384 dimensions

## Next Steps

1. ✅ OpenAI API key configured
2. ✅ Embedding generation working
3. ⏭️ Index code dataset with embeddings
4. ⏭️ Test semantic search

## Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [Embedding Best Practices](https://platform.openai.com/docs/guides/embeddings/use-cases)
