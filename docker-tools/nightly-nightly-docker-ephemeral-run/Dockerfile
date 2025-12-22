FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV RUNNER_VERSION=2.319.1

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    ca-certificates \
    libcurl4 \
    libunwind8 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create runner user
RUN useradd --create-home --shell /bin/bash runner

# Create working directory
WORKDIR /home/runner

# Download and install GitHub Actions runner
RUN curl -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz | tar xz \
    && chown -R runner:runner /home/runner

# Copy scripts
COPY scripts/ ./scripts/
RUN chmod +x scripts/*.sh

# Set entrypoint
ENTRYPOINT ["/home/runner/scripts/entrypoint.sh"]
