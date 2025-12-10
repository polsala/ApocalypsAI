# Dockerfile

FROM ubuntu:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install essential tools and development dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    wget \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /app

# Default command to run when container starts
CMD ["bash"]
