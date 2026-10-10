FROM alpine:3.18

# Install necessary tools: bash, tar, openssl, python3, py3-pip
RUN apk add --no-cache bash tar openssl python3 py3-pip

# Set working directory
WORKDIR /app

# Copy the Python script and entrypoint script
COPY src/chronosync.py /app/chronosync.py
COPY src/entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (will be overridden by user input)
CMD ["--help"]
