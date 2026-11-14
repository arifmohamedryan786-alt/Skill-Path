#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================"
echo "  SkillPath – Your Career Path, From Zero to Job-Ready  "
echo "========================================================"

# 1. Check or create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r backend/requirements.txt
fi

# 2. Check node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# 3. Check or create .env
if [ ! -f ".env" ]; then
    echo "Creating .env configuration from .env.example..."
    cp .env.example .env
fi

# 4. Initialize and seed database if needed
echo "Initializing and verifying database..."
PYTHONPATH=. .venv/bin/python3 -m backend.app.seed.seed_runner

# 5. Trap signals to cleanly shutdown both servers on exit
cleanup() {
    echo ""
    echo "Shutting down SkillPath servers..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 6. Start Backend
echo "Starting FastAPI Backend on http://localhost:8000..."
PYTHONPATH=. .venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend healthcheck..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
        echo "Backend is ready on http://localhost:8000"
        break
    fi
    sleep 0.5
done

# 7. Start Frontend
echo "Starting Vite Frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================================"
echo "  SkillPath is LIVE!"
echo "  - Web Application: http://localhost:5173"
echo "  - Backend API Docs: http://localhost:8000/docs"
echo "  - Health Check:    http://localhost:8000/health"
echo "========================================================"
echo "Press Ctrl+C to stop both servers."

wait

