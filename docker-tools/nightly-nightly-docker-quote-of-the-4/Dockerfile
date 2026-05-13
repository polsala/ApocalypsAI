FROM alpine:3.18

# Install Bash (the only runtime dependency)
RUN apk add --no-cache bash

# Copy the quote script into the image
COPY src/quote.sh /usr/local/bin/quote.sh

# Ensure the script is executable
RUN chmod +x /usr/local/bin/quote.sh

# The container prints a quote and exits
ENTRYPOINT ["/usr/local/bin/quote.sh"]
