#!/bin/bash
set -e

echo "Detecting OS and Environment..."

# Upgrade pip
python3 -m pip install --upgrade pip

# Create and activate .venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi

# Look for software
if ! command -v npm &> /dev/null; then
    echo "Node.js/npm could not be found. Please install via apt install npm."
else
    echo "Node.js found. Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "Launching Platform..."
# Run backend
source .venv/bin/activate
uvicorn backend.app.main:app --reload &

# Run frontend
cd frontend
npm start
