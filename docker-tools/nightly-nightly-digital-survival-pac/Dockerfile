# Use a minimal base image for efficiency
FROM alpine:3.18

# Set labels for better identification
LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized digital survival kit with essential CLI tools."

# Install essential tools
# Use a single RUN command to minimize image layers
# apk add --no-cache is crucial for keeping image size down
RUN apk add --no-cache \
    bash \
    curl \
    jq \
    grep \
    awk \
    sed \
    git \
    htop \
    nmap \
    openssh-client \
    rsync \
    vim \
    coreutils # For 'realpath' and other common utilities

# Set the working directory
WORKDIR /app

# Copy the entrypoint script
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command if none is provided
CMD ["bash"]
