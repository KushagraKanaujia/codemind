# Supabase Setup Guide

This guide walks you through setting up Supabase with pgvector for CodeMind's vector database.

## Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: codemind
   - **Database Password**: (save this securely!)
   - **Region**: Choose closest to you
   - **Plan**: Free tier works for MVP
5. Click "Create new project"
6. Wait 2-3 minutes for provisioning

## Step 2: Enable pgvector Extension

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Run this SQL to enable pgvector:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

4. Click "Run" (you should see "Success")

## Step 3: Create Database Schema

Run this SQL to create the `code_embeddings` table:

```sql
-- Create code_embeddings table
CREATE TABLE code_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT NOT NULL,
    embedding vector(1536), -- OpenAI embedding dimension
    language VARCHAR(50) NOT NULL,
    source TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON code_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for language filtering
CREATE INDEX idx_language ON code_embeddings(language);
```

## Step 4: Create RPC Function for Similarity Search

This function performs vector similarity search:

```sql
-- Function to search for similar code
CREATE OR REPLACE FUNCTION match_code_embeddings(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10,
    filter_language text DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    code TEXT,
    embedding vector(1536),
    language VARCHAR(50),
    source TEXT,
    metadata JSONB,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        ce.id,
        ce.code,
        ce.embedding,
        ce.language,
        ce.source,
        ce.metadata,
        1 - (ce.embedding <=> query_embedding) AS similarity
    FROM code_embeddings ce
    WHERE
        (filter_language IS NULL OR ce.language = filter_language)
        AND (1 - (ce.embedding <=> query_embedding)) > match_threshold
    ORDER BY ce.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

## Step 5: Get API Credentials

1. In Supabase dashboard, go to **Settings** > **API**
2. Copy these values:

   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (under "Project API keys")
   - **service_role key** (under "Project API keys" - keep this secret!)

3. Add to your backend `.env` file:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here
```

## Step 6: Test Connection

You can test the connection using this Python script:

```python
from supabase import create_client

url = "your_supabase_url"
key = "your_supabase_key"

supabase = create_client(url, key)

# Test query
result = supabase.table('code_embeddings').select("*").limit(1).execute()
print("Connection successful!", result.data)
```

## Step 7: Configure Vector Search

Update `backend/app/services/vector_service.py` to use the RPC function:

```python
async def search_similar(
    self,
    query_embedding: List[float],
    limit: int = 10,
    language: Optional[str] = None,
) -> List[Dict]:
    """Search using the match_code_embeddings RPC function."""

    response = self.client.rpc(
        'match_code_embeddings',
        {
            'query_embedding': query_embedding,
            'match_threshold': 0.7,
            'match_count': limit,
            'filter_language': language
        }
    ).execute()

    return response.data
```

## Troubleshooting

### Error: "extension 'vector' does not exist"
- Make sure you ran `CREATE EXTENSION vector;`
- Check you have the right permissions (use service_role key)

### Error: "function match_code_embeddings does not exist"
- Run the RPC function creation SQL again
- Make sure there are no syntax errors

### Slow queries
- Ensure the ivfflat index is created
- For larger datasets (10k+ vectors), consider increasing `lists` parameter
- Run `VACUUM ANALYZE code_embeddings;` periodically

### Connection errors
- Verify your SUPABASE_URL and SUPABASE_KEY are correct
- Check if your IP is allowed (Supabase has no IP restrictions by default)
- Ensure you're using the correct key (anon key for client, service key for admin)

## Next Steps

1. ✅ Database schema created
2. ✅ Vector search function ready
3. ⏭️ Set up OpenAI embeddings (see [EMBEDDINGS.md](./EMBEDDINGS.md))
4. ⏭️ Index your code dataset (see [DATA_INDEXING.md](./DATA_INDEXING.md))
5. ⏭️ Test search functionality

## Resources

- [Supabase pgvector docs](https://supabase.com/docs/guides/database/extensions/pgvector)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Vector similarity functions](https://github.com/pgvector/pgvector#vector-functions)
