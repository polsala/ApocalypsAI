FROM alpine:3.18

# Install Bash (Alpine's default /bin/sh is not sufficient for arrays)
RUN apk add --no-cache bash

# Copy the script into the image
COPY src/tip.sh /usr/local/bin/tip.sh

# Make it executable
RUN chmod +x /usr/local/bin/tip.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/tip.sh"]
