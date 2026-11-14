# Dockerfile for Nightly Resource Scavenger
# This image contains the necessary tools to interact with the Docker daemon
# and analyze container states and resource usage.

FROM alpine:latest

# Install bash and docker-cli
# bash is needed for the scavenger script's advanced features (e.g., string manipulation, arithmetic).
# docker-cli is needed to interact with the Docker daemon via the mounted socket.
RUN apk update && \
    apk add --no-cache bash docker-cli && \
    rm -rf /var/cache/apk/*

# Set the working directory inside the container
WORKDIR /app

# Copy the scavenger script into the container
COPY src/scavenge.sh /app/scavenge.sh

# Make the script executable
RUN chmod +x /app/scavenge.sh

# Define the entrypoint to run the scavenger script. Any arguments passed to the
# 'docker run' command will be forwarded to this entrypoint.
ENTRYPOINT ["/app/scavenge.sh"]
