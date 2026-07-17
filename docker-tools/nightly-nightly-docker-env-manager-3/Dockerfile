# Dockerfile for the ApocalypsAI Docker Env Manager

FROM python:3.11-slim

WORKDIR /app

COPY src/main.py /app/

# Install dependencies
RUN pip install --no-cache-dir docker pyyaml

# Make the script executable
RUN chmod +x /app/main.py

# Define the entrypoint
ENTRYPOINT ["python", "/app/main.py"]

# Default command if none is provided (can be overridden)
CMD ["help"]
