FROM ubuntu:latest

# Install necessary packages: docker.io for the client, bash, coreutils for gdate, and grep for PCRE.
RUN apt-get update && apt-get install -y \
    docker.io \
    bash \
    coreutils \
    grep \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the main script into the container
COPY src/temporal_janitor.sh .

# Make the script executable
RUN chmod +x temporal_janitor.sh

# Set the entrypoint to run the script
ENTRYPOINT ["./temporal_janitor.sh"]
