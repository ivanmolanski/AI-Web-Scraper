# Use an official Python runtime as a parent image based on Debian Bullseye
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # Prevents Python from writing pyc files to disc
    PYTHONDONTWRITEBYTECODE=1 \
    # Set the default port Streamlit will run on (Streamlit Cloud will override with $PORT)
    STREAMLIT_SERVER_PORT=8501

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# Install curl and sudo first for the Ollama script
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Copy packages.txt and install apt packages listed in it
COPY packages.txt .
RUN apt-get update && \
    xargs -a packages.txt apt-get install -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .
# Install uv first, then use it to install requirements
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Expose the port the app runs on
EXPOSE ${STREAMLIT_SERVER_PORT}

# Define the command to run the application using the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
