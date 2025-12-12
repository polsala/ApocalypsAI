# Nightly Docker DevBox - Go Environment
# A whimsical-yet-useful development environment

FROM golang:1.21-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash devuser
RUN chown -R devuser:devuser /app
USER devuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD go version

# Default command
CMD ["/bin/bash"]
