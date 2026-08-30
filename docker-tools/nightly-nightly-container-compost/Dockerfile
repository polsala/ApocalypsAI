FROM alpine:latest

WORKDIR /app

# Install Docker client
# This allows the container to run 'docker' commands, typically against the host's Docker daemon.
# To achieve this, the container must be run with:
#   -v /var/run/docker.sock:/var/run/docker.sock
#   (and potentially --privileged if more permissions are needed, though usually not for basic prune)
RUN apk add --no-cache docker-cli

# Copy the script
COPY src/compost_heap.sh .

# Make the script executable
RUN chmod +x compost_heap.sh

# Define the entrypoint for the container
# This allows running the script directly when the container starts
ENTRYPOINT ["./compost_heap.sh"]

# Default command if no arguments are provided
CMD ["--dry-run"]
