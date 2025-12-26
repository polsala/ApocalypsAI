# Multi-stage Dockerfile for Nightly Docker DevBox
# Base stage with common tools and dependencies
FROM ubuntu:22.04 AS base

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install common tools and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tmux \
    tree \
    unzip \
    zip \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Python stage
FROM base AS python

# Install Python 3.11 and pip
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip3 install --no-cache-dir \
    pytest \
    black \
    flake8 \
    mypy \
    jupyter \
    ipython

# Set Python path
ENV PATH=/usr/local/bin:$PATH

# Rust stage
FROM base AS rust

# Install Rust toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH=/root/.cargo/bin:$PATH

# Install Rust development tools
RUN rustup component add rustfmt clippy
RUN cargo install ripgrep fd-find

# Go stage
FROM base AS go

# Install Go 1.21
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

ENV PATH=/usr/local/go/bin:$PATH
ENV GOPATH=/workspace/go
ENV GOBIN=/workspace/go/bin

# Install Go development tools
RUN go install golang.org/x/tools/cmd/gofmt@latest
RUN go install golang.org/x/tools/cmd/vet@latest
RUN go install github.com/go-delve/delve/cmd/dlv@latest

# Node.js stage
FROM base AS nodejs

# Install Node.js 18+ and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Node.js development tools
RUN npm install -g \
    eslint \
    prettier \
    typescript \
    @types/node

# Java stage
FROM base AS java

# Install OpenJDK 17
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    maven \
    gradle \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# C++ stage
FROM base AS cpp

# Install C++ development tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    clang \
    clang++ \
    gdb \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

# Final stage - combine all languages
FROM base AS final

# Copy language-specific stages
COPY --from=python /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=python /usr/local/bin /usr/local/bin
COPY --from=rust /root/.cargo /root/.cargo
COPY --from=go /usr/local/go /usr/local/go
COPY --from=nodejs /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=nodejs /usr/local/bin/node /usr/local/bin/node
COPY --from=nodejs /usr/local/bin/npm /usr/local/bin/npm
COPY --from=java /usr/lib/jvm/java-17-openjdk-amd64 /usr/lib/jvm/java-17-openjdk-amd64
COPY --from=cpp /usr/bin/gcc /usr/bin/gcc
COPY --from=cpp /usr/bin/g++ /usr/bin/g++
COPY --from=cpp /usr/bin/clang /usr/bin/clang
COPY --from=cpp /usr/bin/clang++ /usr/bin/clang++

# Set environment variables
ENV PATH=/usr/local/go/bin:/root/.cargo/bin:/usr/local/bin:$PATH
ENV GOPATH=/workspace/go
ENV GOBIN=/workspace/go/bin
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Create workspace directory
RUN mkdir -p /workspace/go/bin /workspace/go/src

# Set working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
