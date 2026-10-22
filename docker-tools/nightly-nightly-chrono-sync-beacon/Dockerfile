FROM alpine/git:latest

# Install Docker CLI to interact with the host's Docker daemon
RUN apk add --no-cache docker-cli

# Copy the synchronization script into the image
COPY src/chrono_sync.sh /usr/local/bin/chrono_sync.sh

# Make the script executable
RUN chmod +x /usr/local/bin/chrono_sync.sh

# Set the entrypoint to the synchronization script
ENTRYPOINT ["/usr/local/bin/chrono_sync.sh"]
