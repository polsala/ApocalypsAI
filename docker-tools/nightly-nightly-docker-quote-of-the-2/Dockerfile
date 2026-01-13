FROM alpine:3.18

# Copy the quote script into the image
COPY src/quote.sh /usr/local/bin/quote.sh

# Ensure the script is executable
RUN chmod +x /usr/local/bin/quote.sh

# Set the script as the container's entrypoint
ENTRYPOINT [\"/usr/local/bin/quote.sh\"]
