#!/bin/bash

# AI-Eye Watcher Backend Setup Script

echo "Setting up AI-Eye Watcher Backend..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the server:"
echo "1. source venv/bin/activate"
echo "2. uvicorn central_server:app --reload --port 9000"
echo "3. Visit http://localhost:9000/docs for API documentation"