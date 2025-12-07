FROM alpine:latest

# Install necessary tools
RUN apk add --no-cache bash findutils coreutils

# Create working directory
WORKDIR /app

# Copy the sweeper script
COPY src/sweeper.sh /app/sweeper.sh
RUN chmod +x /app/sweeper.sh

# Set entry point
ENTRYPOINT ["/app/sweeper.sh"]
