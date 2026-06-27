#!/bin/bash

# CodeMind Setup Script
# Automates the initial setup process

set -e

echo "🧠 CodeMind Setup Script"
echo "========================"
echo ""

# Check if in codemind directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the codemind directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate

echo "  Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "  Creating .env file from template..."
    cp .env.example .env
    echo "  ⚠️  IMPORTANT: Edit backend/.env and add your API keys!"
fi

cd ..

# Frontend setup
echo ""
echo "🎨 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "  Installing Node dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "  Creating .env file from template..."
    cp .env.example .env
fi

cd ..

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/raw data/processed

# Git setup
echo ""
echo "🔧 Initializing Git repository..."
if [ ! -d ".git" ]; then
    git init
    git add .
    echo "  Git repository initialized"
else
    echo "  Git repository already exists"
fi

# Summary
echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Add your API keys to backend/.env:"
echo "   - ANTHROPIC_API_KEY (get from: https://console.anthropic.com)"
echo "   - OPENAI_API_KEY (get from: https://platform.openai.com)"
echo ""
echo "2. Set up Supabase (see docs/SUPABASE_SETUP.md)"
echo "   - Create project at https://supabase.com"
echo "   - Enable pgvector extension"
echo "   - Add credentials to backend/.env"
echo ""
echo "3. Start the development servers:"
echo "   Terminal 1 (backend):"
echo "     cd backend"
echo "     source venv/bin/activate"
echo "     uvicorn app.main:app --reload"
echo ""
echo "   Terminal 2 (frontend):"
echo "     cd frontend"
echo "     npm run dev"
echo ""
echo "4. Visit http://localhost:5173 in your browser"
echo ""
echo "📚 Documentation:"
echo "   - Supabase setup: docs/SUPABASE_SETUP.md"
echo "   - Embeddings setup: docs/EMBEDDINGS.md"
echo "   - Deployment: docs/DEPLOYMENT.md"
echo ""
echo "🎉 Happy coding!"
