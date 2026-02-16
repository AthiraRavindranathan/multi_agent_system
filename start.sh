#!/bin/bash

# Start script for Multi-Agent Support System

echo "Starting Multi-Agent Support System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting server on http://localhost:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
