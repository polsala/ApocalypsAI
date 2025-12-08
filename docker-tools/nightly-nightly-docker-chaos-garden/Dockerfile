FROM python:3.11-slim

# Install Docker client for API access
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install docker pyyaml

# Set working directory
WORKDIR /app

# Copy application files
COPY src/ ./src/
COPY requirements.txt .

# Create output directory
RUN mkdir -p /app/reports

# Set executable permissions
RUN chmod +x /app/src/chaos_garden.py

# Default command
CMD ["python", "/app/src/chaos_garden.py"]
