FROM alpine:3.18

# Install bash (Alpine's default shell is ash, but we use bash for readability)
RUN apk add --no-cache bash

# Copy the entrypoint script into the image
COPY src/entrypoint.sh /entrypoint.sh

# Make it executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
