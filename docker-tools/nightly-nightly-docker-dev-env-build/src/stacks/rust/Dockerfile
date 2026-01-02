# Rust Development Environment
FROM rust:1.75-slim

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust development tools
RUN rustup component add rustfmt clippy rust-analyzer

# Set working directory
WORKDIR /app

# Expose default port
EXPOSE 3000

# Default command
CMD ["cargo", "--help"]
