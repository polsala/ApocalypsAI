FROM ubuntu:22.04

LABEL maintainer="ApocalypsAI Integrator <integrator@apoc.ai>"

# Install common build tools and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-venv \
    && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3.11 /usr/bin/python3
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Rust 1.70
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain 1.70.0 && \
    cargo install --version 0.1.24 cargo-edit && \
    rm -rf /root/.cargo/registry/* /root/.cargo/git/*

# Install Go 1.21
RUN curl -fsSL https://dl.google.com/go/go1.21.5.linux-amd64.tar.gz | tar -xz -C /usr/local
ENV PATH="/usr/local/go/bin:${PATH}"

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["bash"]
