#!/bin/bash

echo "🎮 Starting CodeMind in DEMO MODE (No API Keys Required!)"
echo "=========================================================="
echo ""

# Copy demo env file
cp backend/.env.demo backend/.env
echo "✅ Using demo configuration (no real API keys needed)"
echo ""

# Check if backend dependencies are installed
if [ ! -d "backend/venv" ]; then
    echo "📦 Setting up backend..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Setting up frontend..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🚀 Starting servers..."
echo ""
echo "This will open TWO terminal windows:"
echo "  1. Backend (http://localhost:8000)"
echo "  2. Frontend (http://localhost:5173)"
echo ""

# Start backend in new terminal
echo "Starting backend..."
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"'/backend && source venv/bin/activate && echo \"🔧 Backend running at http://localhost:8000\" && echo \"📚 API docs at http://localhost:8000/docs\" && echo \"\" && uvicorn app.main:app --reload"'

# Wait a moment
sleep 2

# Start frontend in new terminal
echo "Starting frontend..."
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"'/frontend && echo \"🎨 Frontend running at http://localhost:5173\" && echo \"\" && npm run dev"'

sleep 3

echo ""
echo "✅ CodeMind DEMO is starting!"
echo ""
echo "📖 What you can do in DEMO mode:"
echo "   • Explore the full UI"
echo "   • Try searches (e.g., 'binary search', 'sorting')"
echo "   • See simulated Claude reasoning"
echo "   • Understand the app flow"
echo ""
echo "⚠️  What's mocked:"
echo "   • API calls (using fake responses)"
echo "   • Only ~5 demo code examples"
echo "   • Database searches"
echo ""
echo "🔑 To use REAL mode:"
echo "   1. Get API keys (see API_KEYS_SETUP.md)"
echo "   2. Run ./setup.sh instead"
echo ""
echo "🌐 Opening browser in 5 seconds..."
sleep 5
open http://localhost:5173

echo ""
echo "Happy experimenting! 🎉"
