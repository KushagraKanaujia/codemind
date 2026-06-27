# Getting Started with CodeMind

Welcome! This guide will get you up and running with CodeMind in under 30 minutes.

## What You'll Build

By the end of this guide, you'll have:
- ✅ A working semantic code search engine
- ✅ Claude AI analyzing and ranking code implementations
- ✅ Beautiful UI showing results with explanations
- ✅ Vector database with embeddings
- ✅ Everything running locally

## Prerequisites

Make sure you have these installed:
- **Python 3.9+** (`python3 --version`)
- **Node.js 18+** (`node --version`)
- **Git** (`git --version`)

And these accounts (free tier works):
- [Anthropic API key](https://console.anthropic.com) - for Claude AI
- [OpenAI API key](https://platform.openai.com) - for embeddings
- [Supabase account](https://supabase.com) - for vector database

## Quick Start (5 minutes)

### Step 1: Run Setup Script

```bash
cd codemind
./setup.sh
```

This installs all dependencies and creates config files.

### Step 2: Add API Keys

Edit `backend/.env` and add your keys:

```bash
# Get from https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Get from https://platform.openai.com
OPENAI_API_KEY=sk-xxxxx

# We'll set up Supabase next
SUPABASE_URL=
SUPABASE_KEY=
```

### Step 3: Set Up Supabase (15 minutes)

Follow the **[Supabase Setup Guide](docs/SUPABASE_SETUP.md)** to:
1. Create a Supabase project (2 min)
2. Enable pgvector extension (1 min)
3. Create database schema (2 min)
4. Get API credentials (1 min)
5. Add credentials to `.env` (1 min)

Once done, your `.env` should look like:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 4: Index Sample Data

Load the sample code examples into your database:

```bash
cd backend
source venv/bin/activate
python scripts/index_code_data.py --data-file ../data/sample_code.json
```

You should see:
```
Successfully indexed: 10
Failed: 0
Total: 10
```

### Step 5: Start the Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 6: Try It Out!

1. Open http://localhost:5173
2. Try searching: "binary search algorithm"
3. Watch Claude analyze and rank results!

## What Just Happened?

1. **You searched** for "binary search algorithm"
2. **OpenAI generated** an embedding vector for your query
3. **Supabase found** similar code using vector similarity
4. **Claude analyzed** each result, explained what it does
5. **Claude ranked** them based on your criteria
6. **You saw** ranked results with reasoning!

That's the power of semantic search + AI reasoning ✨

## Next Steps

### Add More Code Examples

Edit `data/sample_code.json` to add your own:

```json
{
  "code": "your code here",
  "language": "python",
  "source": "my_project/file.py",
  "description": "What this code does"
}
```

Then run the indexer again:
```bash
python scripts/index_code_data.py --data-file ../data/sample_code.json
```

### Customize the Ranking

When searching, add criteria like:
- "fast" - prioritize performance
- "readable" - prioritize clarity
- "secure" - prioritize safety
- "simple" - prioritize simplicity

Claude will rank based on these!

### Deploy to Production

When ready, follow the **[Deployment Guide](docs/DEPLOYMENT.md)** to:
- Deploy backend to Railway
- Deploy frontend to Vercel
- Set up custom domains
- Configure CI/CD

## Troubleshooting

### "Error: No API key provided"
- Check your `.env` file has all keys
- Make sure keys don't have quotes: `KEY=value` not `KEY="value"`
- Restart backend after changing `.env`

### "Connection to Supabase failed"
- Verify SUPABASE_URL and SUPABASE_KEY are correct
- Check you enabled pgvector extension
- Try the connection test in [SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)

### "No results found" when searching
- Make sure you indexed data: `python scripts/index_code_data.py`
- Check backend logs for errors
- Verify Supabase table has data (use Supabase dashboard)

### Backend won't start
- Check Python version: `python3 --version` (need 3.9+)
- Activate venv: `source venv/bin/activate`
- Check for port conflicts: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and run `npm install` again
- Check for port conflicts: `lsof -i :5173`

## Project Structure

```
codemind/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── services/     # Claude + Vector services
│   │   ├── models/       # Data models
│   │   └── core/         # Config
│   └── scripts/          # Utility scripts
├── frontend/             # React frontend
│   └── src/
│       ├── components/   # UI components
│       ├── pages/        # Pages
│       └── services/     # API client
├── data/                 # Code datasets
└── docs/                 # Documentation
```

## Key Files

- `backend/app/services/claude_service.py` - Claude AI integration
- `backend/app/services/vector_service.py` - Supabase vector search
- `backend/app/api/search.py` - Search API endpoint
- `frontend/src/pages/SearchPage.tsx` - Search UI
- `frontend/src/components/SearchResults.tsx` - Results display

## Common Tasks

### View Backend Logs
```bash
# Backend runs in foreground, logs print to terminal
# Look for errors like "Error generating embedding"
```

### View Database Contents
Go to Supabase dashboard → Table Editor → code_embeddings

### Clear Database
```sql
DELETE FROM code_embeddings;
```

Then re-index: `python scripts/index_code_data.py`

### Update Dependencies
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

## Understanding the Code Flow

1. **User types query** → SearchPage.tsx
2. **Frontend calls API** → api.ts → `/api/v1/search/`
3. **Backend generates embedding** → claude_service.py
4. **Search vector DB** → vector_service.py → Supabase
5. **Claude ranks results** → claude_service.py (rank_code_results)
6. **Return to frontend** → SearchResults.tsx
7. **Display with explanations** → User sees results!

## Cost Tracking

At low volume (MVP):
- **OpenAI embeddings**: ~$0.02 per 1000 queries
- **Claude API**: ~$0.003 per query (text generation)
- **Supabase**: Free (under 500MB)

For 1000 queries: **~$3/month** 💰

## Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: Check GitHub issues
- **Community**: (Add your Discord/Slack if you have one)

## What's Next?

You've completed **Week 1** of the CodeMind roadmap! 🎉

Next up (Week 2): **AI System Testing Agent**
- Auto-generate test cases for prompts
- Categorize failures
- Suggest improvements
- Track improvements over time

Stay tuned!

## Feedback

Found a bug? Have a suggestion? Open an issue on GitHub!

This project is part of a portfolio to demonstrate:
- Semantic search with LLM reasoning
- Clean architecture for AI applications
- Production-ready deployment

---

**Built with Claude AI • Not a chatbot wrapper, a reasoning engine** 🧠
