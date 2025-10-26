#!/bin/bash

# AI-Eye Watcher Agent Setup Script for macOS

echo "Setting up AI-Eye Watcher Agent..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Create virtual environment for the agent
echo "Creating virtual environment..."
python3 -m venv agent_venv

# Activate virtual environment
echo "Activating virtual environment..."
source agent_venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install -r agent_requirements.txt

echo "Setup complete!"
echo ""
echo "To run the agent:"
echo "1. Activate the virtual environment: source agent_venv/bin/activate"
echo "2. Run the agent: python3 agent.py"
echo ""
echo "Note: You may need to run with sudo for process killing capabilities:"
echo "sudo ./agent_venv/bin/python agent.py"