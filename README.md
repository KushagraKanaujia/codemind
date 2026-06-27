# CodeMind

**Semantic code search + AI system testing agent**

CodeMind is not another ChatGPT wrapper. It's a reasoning engine that:
1. **Searches code semantically** - finds implementations, ranks them by criteria, explains trade-offs
2. **Tests AI systems autonomously** - generates test cases, identifies failures, suggests improvements

## Differentiation

- ✅ **Semantic understanding**: Not keyword search, actual code semantics
- ✅ **Autonomous testing**: Claude generates and runs tests automatically
- ✅ **Iterative improvement**: Test → improve → test again cycle
- ✅ **Reasoning transparency**: See *why* results are ranked, not just what they are

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Anthropic API key
- Supabase account

### Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

See `.env.example` for required configuration.

## Architecture

```
codemind/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Config, dependencies
│   │   ├── services/ # Business logic
│   │   ├── models/   # Data models
│   │   └── utils/    # Helpers
│   └── tests/        # Unit tests
├── frontend/         # React + Vite frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
└── data/             # Code datasets
    ├── raw/          # Original code examples
    └── processed/    # Embedded vectors
```

## Features

### Week 1: Semantic Code Search (Current)
- Natural language → code search
- Claude analyzes and ranks results
- Explains trade-offs between implementations

### Week 2: AI System Testing (Coming)
- Auto-generate test cases
- Categorize failures
- Suggest prompt improvements

## Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Frontend**: React, Vite, TypeScript
- **AI**: Anthropic Claude API
- **Vector DB**: Supabase pgvector
- **Cache**: Redis
- **Deploy**: Vercel (frontend), Railway (backend)

## Development

```bash
# Run tests
cd backend
pytest

# Format code
black app/
isort app/

# Type check
mypy app/
```

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## Contributing

This is a portfolio project focused on demonstrating:
- Semantic search with LLM reasoning
- Autonomous testing of AI systems
- Clean architecture for AI applications

## License

MIT
