#!/usr/bin/env bash
# Start the CodeMind API (http://localhost:8000) and UI (http://localhost:5173) together.
# Works with zero API keys: the UI uses the backend's /demo endpoints and falls back
# to in-browser search if the API isn't up. Add keys to backend/.env and set
# VITE_SEARCH_MODE=live to use Claude-ranked search.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

(cd "$ROOT/backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000) &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT

cd "$ROOT/frontend"
[ -d node_modules ] || npm ci
npm run dev -- --host 0.0.0.0
