FROM alpine:latest

# Install Docker CLI
RUN apk add --no-cache docker

# Copy the script
COPY src/compost.sh /usr/local/bin/compost.sh

# Make it executable
RUN chmod +x /usr/local/bin/compost.sh

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/compost.sh"]
