FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    ca-certificates \
    apt-transport-https \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce-cli

# Create working directory
WORKDIR /app

# Copy application files
COPY runner.sh /app/runner.sh
COPY config.sh /app/config.sh
COPY health-check.sh /app/health-check.sh
COPY cleanup.sh /app/cleanup.sh

# Make scripts executable
RUN chmod +x /app/runner.sh /app/config.sh /app/health-check.sh /app/cleanup.sh

# Set environment variables
ENV RUNNER_VERSION=2.320.2
ENV RUNNER_OS=linux
ENV RUNNER_ARCH=x64

# Download and extract GitHub Actions runner
RUN curl -L -o actions-runner.tar.gz \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-${RUNNER_OS}-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" \
    && tar xzf ./actions-runner.tar.gz \
    && rm actions-runner.tar.gz

# Set entrypoint
ENTRYPOINT ["/app/runner.sh"]
