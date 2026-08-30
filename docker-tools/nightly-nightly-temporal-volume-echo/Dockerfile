FROM alpine:latest

# Install bash, tar, and docker-cli for interacting with the Docker daemon
RUN apk add --no-cache bash tar docker-cli

# Copy the echo manager script into the image
COPY src/echo_manager.sh /usr/local/bin/echo_manager.sh

# Make the script executable
RUN chmod +x /usr/local/bin/echo_manager.sh

# Set the entrypoint to the script, so it runs when the container starts
ENTRYPOINT ["/usr/local/bin/echo_manager.sh"]
# Provide a default command if no arguments are given
CMD ["help"]
