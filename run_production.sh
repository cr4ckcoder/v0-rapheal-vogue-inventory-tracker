#!/bin/bash
# Production startup script

echo "Starting Rapheal Vogue Inventory Tracker (Production)"

# Start backend with Gunicorn
echo "Starting backend..."
gunicorn -w 4 -b 0.0.0.0:8000 main:app &
BACKEND_PID=$!

# Start frontend (if needed)
# cd frontend && npm run build && npm run preview &
# FRONTEND_PID=$!

echo "Backend running (PID: $BACKEND_PID)"
echo "API available at: http://0.0.0.0:8000"
echo "API docs at: http://0.0.0.0:8000/docs"

# Keep running
wait
