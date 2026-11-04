# 🎮 Demo Mode - No API Keys Required!

Try CodeMind right now without setting up API keys or databases!

## 🚀 Quick Start (2 minutes)

### Option 1: Automatic (macOS)

```bash
cd codemind
./start-demo.sh
```

This script will:
- ✅ Set up demo configuration
- ✅ Install dependencies if needed
- ✅ Start both backend and frontend
- ✅ Open your browser automatically

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd codemind/backend

# Copy demo config
cp .env.demo .env

# Set up environment (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd codemind/frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Terminal 3 - Open Browser:**
```bash
open http://localhost:5173
```

---

## 🎯 What You Can Do

### Try These Searches:

1. **"binary search"**
   - See 3 implementations (Python, JavaScript, C)
   - Watch Claude's analysis and ranking
   - View score breakdowns

2. **"sorting algorithm"**
   - See quicksort vs mergesort
   - Compare performance trade-offs
   - See detailed explanations

3. **Any other query**
   - Will show generic demo result
   - Still demonstrates the UI flow

### Explore The UI:

- ✅ Search bar with filters
- ✅ Criteria selection (fast, readable, secure, etc.)
- ✅ Language filtering
- ✅ Beautiful code syntax highlighting
- ✅ Claude's reasoning explanations
- ✅ Score breakdowns with visual bars
- ✅ Ranking reasons

---

## 📊 What's Working vs What's Mocked

### ✅ Working (Real):
- Full UI functionality
- Search interface
- Filters and criteria
- Code highlighting
- Responsive design
- All components

### 🎭 Mocked (Simulated):
- API calls to Claude (using fake responses)
- OpenAI embeddings (not generated)
- Vector database search (pre-defined results)
- Only ~5 demo examples (vs 203 real ones)

---

## 🎨 Demo Screenshots

What you'll see:

**Search Results:**
```
Found 3 results for "binary search" in 125ms

🧠 Claude's Analysis:
I analyzed these code implementations and ranked them...
[Shows detailed reasoning]

#1 Python Implementation
Why this rank: Most Pythonic, perfect balance...
[Code with syntax highlighting]
Scores: fast: 9/10, readable: 10/10, simple: 9/10

#2 JavaScript Implementation
...
```

---

## 🔄 Switch to Real Mode (When You Have API Keys)

1. **Get API keys:**
   - See `API_KEYS_SETUP.md` for step-by-step guide
   - Anthropic: https://console.anthropic.com
   - OpenAI: https://platform.openai.com

2. **Update `.env`:**
   ```bash
   cd backend
   # Edit .env with real keys
   nano .env
   ```

3. **Set up Supabase:**
   - Follow `docs/SUPABASE_SETUP.md`

4. **Index real data:**
   ```bash
   python scripts/index_code_data.py --data-file ../data/complete_dataset.json
   ```

5. **Restart and enjoy 203 real examples!**

---

## 🐛 Troubleshooting

### Backend won't start:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend won't start:
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### "Module not found":
Make sure you're in the virtual environment:
```bash
source backend/venv/bin/activate
```

### Port already in use:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

---

## 📖 Understanding the Demo

### What Happens When You Search:

1. **You type:** "binary search"
2. **Frontend sends** POST to `/api/v1/demo/search`
3. **Backend checks** query keywords
4. **Returns** pre-written mock results
5. **Frontend displays** with full UI

### Demo Data Location:
`backend/app/api/demo.py` - Contains all mock responses

### How It Differs from Real:

| Feature | Demo Mode | Real Mode |
|---------|-----------|-----------|
| Search queries | Keyword matching | Semantic similarity |
| Code examples | 5 hardcoded | 203 in database |
| Analysis | Pre-written | Claude generates |
| Embeddings | None | OpenAI generates |
| Response time | Instant | ~2-3 seconds |
| Cost | $0 | ~$0.003/search |

---

## 🎓 What You're Learning

Even in demo mode, you can:

- ✅ See how semantic search UX should work
- ✅ Understand code ranking by criteria
- ✅ Experience LLM reasoning explanations
- ✅ Explore the architecture
- ✅ Understand the data flow
- ✅ Test the frontend components
- ✅ Prepare for the real thing!

---

## 🎯 Next Steps

Once you've explored demo mode:

1. **Understand the value** - See why this is better than Google
2. **Get inspired** - Think of what else you could search
3. **Get API keys** - It's worth it! ($5 Anthropic credit free)
4. **Go production** - Index 203 real examples
5. **Build Week 2** - Add the testing agent feature

---

## 💬 Demo Mode FAQ

**Q: Can I add my own demo results?**
A: Yes! Edit `backend/app/api/demo.py` and add to `DEMO_RESULTS`

**Q: Does this count against API quotas?**
A: No! Demo mode makes zero real API calls

**Q: Can I deploy this to show others?**
A: Yes! Deploy to Railway/Vercel in demo mode (free)

**Q: How do I know I'm in demo mode?**
A: Check the Claude reasoning - it says "DEMO MODE"

**Q: Will my searches be saved?**
A: No - everything is ephemeral in demo mode

---

**Ready to try it?** Just run `./start-demo.sh` and start experimenting! 🎉

No credit card. No API keys. No database. Just pure exploration!
