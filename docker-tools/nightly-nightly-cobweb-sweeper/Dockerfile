# Use a minimal base image with common utilities
FROM alpine:3.18

# Install necessary tools: bash, findutils, grep, coreutils (for du)
RUN apk add --no-cache bash findutils grep coreutils

# Copy the scanner script into the container
COPY src/cobweb_scanner.sh /usr/local/bin/cobweb_scanner.sh

# Make the script executable
RUN chmod +x /usr/local/bin/cobweb_scanner.sh

# Set the entrypoint to the scanner script
# This allows passing arguments directly to the script, e.g., the target directory
ENTRYPOINT ["/usr/local/bin/cobweb_scanner.sh"]

# Default command if no arguments are provided (scans /scan_target)
CMD ["/scan_target"]
