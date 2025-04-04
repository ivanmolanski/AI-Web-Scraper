#!/bin/bash

# Start Ollama server in the background
echo "Starting Ollama server..."
/usr/local/bin/ollama serve &

# Wait a few seconds for Ollama to start
echo "Waiting for Ollama server to initialize..."
sleep 5 

# Check if Ollama is running (optional but good practice)
if curl http://localhost:11434 > /dev/null 2>&1; then
  echo "Ollama server started successfully."
else
  echo "Ollama server failed to start. Check logs."
  # Optionally exit if Ollama is critical
  # exit 1 
fi

# Execute the Streamlit command
# Streamlit Cloud will set the PORT environment variable, so we use that.
echo "Starting Streamlit app on port $PORT..."
streamlit run main.py --server.port $PORT --server.address 0.0.0.0
