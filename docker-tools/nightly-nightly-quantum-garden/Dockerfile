FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/ ./src/
COPY tests/ ./tests/

# Set entry point
ENTRYPOINT ["python3", "/app/src/main.py"]

# Default command
CMD []
