#!/bin/bash
# NVMe Requirement Tool - Backend & Frontend 동시 실행

echo "Starting NVMe Requirement Manager..."

# Backend
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate
fi

echo "Starting backend on :8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Frontend
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend on :5173..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Backend:  http://localhost:8000 (API docs: http://localhost:8000/docs)"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
