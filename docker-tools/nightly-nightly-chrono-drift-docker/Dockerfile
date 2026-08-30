# Use a slim Debian base image for a balance of size and package availability
FROM debian:stable-slim

# Install faketime and any other necessary utilities
RUN apt-get update && \
    apt-get install -y faketime procps && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script
COPY src/entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]
