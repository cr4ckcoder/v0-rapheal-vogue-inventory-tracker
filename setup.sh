#!/bin/bash
# Quick setup script for Rapheal Vogue Inventory Tracker

echo "Rapheal Vogue Inventory Tracker - Setup"
echo "========================================"

# Backend setup
echo ""
echo "Setting up backend..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create initial admin user
echo ""
echo "Creating initial admin user..."
python << 'EOF'
from database import init_db, get_db
from auth import hash_password

init_db()

with get_db() as conn:
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            ("admin", hash_password("admin123"))
        )
        conn.commit()
        print("✓ Admin user created (username: admin, password: admin123)")
    except:
        print("✓ Admin user already exists")
EOF

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "To start the backend: python run.py"
echo "To start the frontend: cd frontend && npm run dev"
echo ""
echo "Backend will be at: http://localhost:8000"
echo "Frontend will be at: http://localhost:5173"
echo "API docs at: http://localhost:8000/docs"
