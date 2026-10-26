FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized utility to sweep away unused Docker images, containers, and volumes."

# Install Docker CLI
# We need the Docker client inside the container to interact with the host's Docker daemon.
RUN apk add --no-cache docker

# Copy the sweep script into the container
COPY src/sweep.sh /usr/local/bin/sweep.sh

# Make the script executable
RUN chmod +x /usr/local/bin/sweep.sh

# Set the entrypoint to the sweep script
ENTRYPOINT ["/usr/local/bin/sweep.sh"]
