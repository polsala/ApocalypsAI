FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./
COPY config.yaml ./

# Create directory for logs
RUN mkdir -p /app/logs

# Set permissions
RUN chmod +x main.py

# Expose port for potential web dashboard (future feature)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import docker; docker.from_env().ping()" || exit 1

# Default command
CMD ["python", "main.py"]
