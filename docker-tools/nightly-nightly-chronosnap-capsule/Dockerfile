FROM alpine/git:latest

# Install necessary tools: bash, tar, gzip, coreutils (for date)
RUN apk add --no-cache bash tar gzip coreutils

# Create directories for target data and snapshots
# These will be mounted as volumes from the host
RUN mkdir -p /data /snapshots

# Copy the entrypoint script
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define default environment variables (can be overridden at runtime)
ENV TARGET_DIR="/data"
ENV SNAPSHOT_ROOT_DIR="/snapshots"

# Default command if none is specified (keeps container running for exec commands)
CMD ["tail", "-f", "/dev/null"]
