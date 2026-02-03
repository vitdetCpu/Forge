#!/bin/bash

echo "🚀 Interview Prep Agent - Quick Start"
echo "====================================="
echo ""

# Check if Redis is running
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis not found. Please install Redis first:"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    echo "   Docker: docker run -d -p 6379:6379 redis:latest"
    exit 1
fi

if ! redis-cli ping &> /dev/null; then
    echo "⚠️  Redis is not running. Starting Redis..."
    if command -v brew &> /dev/null; then
        brew services start redis
    else
        echo "Please start Redis manually: redis-server"
        exit 1
    fi
fi

echo "✅ Redis is running"
echo ""

# Setup backend
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys!"
    echo ""
fi

echo "✅ Backend setup complete"
echo ""

# Setup frontend
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
fi

echo "✅ Frontend setup complete"
echo ""

# Generate demo data
echo "📊 Generating demo data..."
cd ../backend
source venv/bin/activate
python generate_demo_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
