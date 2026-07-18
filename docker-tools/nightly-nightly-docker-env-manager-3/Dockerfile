# Dockerfile for ApocalypsAI Docker Environment Manager

FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (using nodesource)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Go (latest stable)
RUN wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz && \
    rm go1.22.5.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
