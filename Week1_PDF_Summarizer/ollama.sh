#!/bin/bash

# Script to check if Ollama is installed and running
# If not installed, it will guide the user to install it
# If installed, it will start ollama serve

echo "Checking for Ollama installation..."

# Check if ollama command exists
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo ""
    echo "To install Ollama, please visit: https://ollama.ai"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

echo "✓ Ollama is installed"

# Check if ollama server is already running
echo "Checking if Ollama server is running..."

if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✓ Ollama server is already running at http://localhost:11434"
    exit 0
fi

echo "Starting Ollama server..."
echo ""
echo "Note: This will keep running in the foreground. Press Ctrl+C to stop."
echo ""

# Start ollama serve
ollama serve