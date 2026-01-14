# Use a lightweight base image
FROM alpine:latest

# Install necessary tools: yamllint for YAML linting and a basic HTTP client for potential future needs
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    yamllint \
    curl \
    jq

# Install action-validator for GitHub Actions workflow validation
RUN pip3 install action-validator

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]
