FROM alpine:3.18

# Install Bash (the script relies on it)
RUN apk add --no-cache bash

# Copy the entrypoint script into the image
COPY src/entrypoint.sh /entrypoint.sh

# Ensure the script is executable
RUN chmod +x /entrypoint.sh

# Run the script when the container starts
ENTRYPOINT ["/entrypoint.sh"]
