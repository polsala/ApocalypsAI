# Dockerfile for Nightly Docker Environment Manager

# Stage 1: Builder - Install common development tools
FROM python:3.11-slim AS builder

LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install common development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    nano \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python build tools (if needed for specific packages)
RUN pip install --no-cache-dir \
    build \
    wheel \
    setuptools

# Create a non-root user for better security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Set a default working directory
WORKDIR /app

# Stage 2: Final Image - Copy from builder stage
FROM builder AS final

# Stage 3: Test Stage
FROM final AS test

# Verify installation of key tools
RUN git --version \
    && curl --version \
    && vim --version \
    && nano --version \
    && wget --version \
    && python --version

# Add a simple test script to verify basic functionality
COPY tests/test_env_manager.sh /usr/local/bin/test_env_manager.sh
RUN chmod +x /usr/local/bin/test_env_manager.sh

# Entrypoint for testing
ENTRYPOINT ["/usr/local/bin/test_env_manager.sh"]
