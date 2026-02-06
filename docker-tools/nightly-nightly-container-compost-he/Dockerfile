# Use a minimal base image
FROM alpine:3.18

# Install Docker CLI
RUN apk add --no-cache docker

# Set working directory
WORKDIR /app

# Copy the pruning script
COPY src/prune.sh /app/prune.sh

# Make the script executable
RUN chmod +x /app/prune.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/app/prune.sh"]
