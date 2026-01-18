FROM alpine/git:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A Dockerized ephemeral command execution environment with snapshot/restore."

# Install necessary tools
RUN apk add --no-cache bash coreutils tar gzip

# Set working directory
WORKDIR /workspace

# Copy the entrypoint script
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define default command if none is provided
CMD ["bash"]

# Entrypoint for snapshot/restore operations
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
