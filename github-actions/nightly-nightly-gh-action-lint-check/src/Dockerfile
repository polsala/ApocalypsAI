# Use a lightweight base image
FROM alpine:latest

# Install necessary tools: yamllint, jq (for schema validation), and git
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    git \
    && pip3 install --no-cache-dir yamllint jq \
    && apk del py3-pip \
    && rm -rf /var/cache/apk/*

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
