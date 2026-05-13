FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized, ephemeral development/survival environment with essential CLI tools."

# Install essential tools
RUN apk update && \
    apk add --no-cache \
    bash \
    git \
    nano \
    less \
    tar \
    gzip \
    unzip \
    curl \
    wget \
    jq \
    grep \
    sed \
    awk \
    python3 \
    py3-pip \
    # Clean up apk cache
    && rm -rf /var/cache/apk/*

# Set a working directory
WORKDIR /workspace

# Default command to run bash
CMD ["bash"]
