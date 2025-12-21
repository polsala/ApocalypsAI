FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A minimalist, containerized development environment with optional zen mode."

# Install essential tools
RUN apk add --no-cache bash git vim nano

# Create a directory for our scripts
WORKDIR /app

# Copy scripts
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY src/zen_mode.sh /usr/local/bin/zen_mode.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/zen_mode.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command if no other is specified
CMD ["bash"]
