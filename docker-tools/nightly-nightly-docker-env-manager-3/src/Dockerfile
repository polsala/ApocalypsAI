# Dockerfile for the Nightly Docker Env Manager

FROM alpine:latest

RUN apk add --no-cache docker docker-cli

# Install a basic shell and utilities
RUN apk add --no-cache bash curl

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
