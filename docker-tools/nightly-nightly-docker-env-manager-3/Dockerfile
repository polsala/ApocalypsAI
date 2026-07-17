# Dockerfile for Nightly Docker Env Manager

FROM alpine:latest

# Install necessary packages
RUN apk update && apk add --no-cache docker-compose bash

# Copy the manager script
COPY src/docker-env-manager /usr/local/bin/docker-env-manager

# Make the script executable
RUN chmod +x /usr/local/bin/docker-env-manager

# Set the entrypoint to the manager script
ENTRYPOINT ["docker-env-manager"]

# Default command if none is provided (e.g., to show help)
CMD ["--help"]
