FROM alpine:3.18

# Install coreutils for wc and other utilities (already present in Alpine)
RUN apk add --no-cache bash

# Copy the fortune script into the image
COPY src/fortune.sh /usr/local/bin/fortune.sh

# Ensure the script is executable
RUN chmod +x /usr/local/bin/fortune.sh

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/fortune.sh"]
