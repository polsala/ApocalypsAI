FROM alpine:3.18

# Install bash for the script
RUN apk add --no-cache bash

# Copy the fortune script into the image
COPY src/fortune.sh /usr/local/bin/fortune.sh
RUN chmod +x /usr/local/bin/fortune.sh

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/fortune.sh"]
