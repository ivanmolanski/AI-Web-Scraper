#!/bin/bash

# Find ollama executable
OLLAMA_PATH=$(which ollama)

if [ -z "$OLLAMA_PATH" ]; then
  echo "Error: Ollama executable not found in PATH."
  exit 1
fi

echo "Found Ollama at: $OLLAMA_PATH"

# Start Ollama server in the background
echo "Starting Ollama server..."
nohup $OLLAMA_PATH serve > ollama.log 2>&1 &

# Wait longer for Ollama to start
echo "Waiting 15 seconds for Ollama server to initialize..."
sleep 15

# Check if Ollama is running and pull the model
echo "Checking Ollama status and pulling model..."
if $OLLAMA_PATH run llama3.1 --version > /dev/null 2>&1; then
  echo "Ollama server seems to be running and model is available/pulled."
else
  echo "Ollama server failed to start, respond, or pull the model."
  echo "--- Ollama Log ---"
  cat ollama.log || echo "ollama.log not found or empty."
  echo "------------------"
  # Exit if Ollama failed to start, as the app depends on it.
  exit 1
fi

# Execute the Streamlit command
# Streamlit Cloud will set the PORT environment variable, so we use that.
# Use exec to replace the shell process with the Streamlit process
echo "Starting Streamlit app on port $PORT..."
exec streamlit run main.py --server.port $PORT --server.address 0.0.0.0
