FROM alpine:latest

# Install bash and coreutils for a more robust shell environment
RUN apk add --no-cache bash coreutils

# Set the working directory
WORKDIR /app

# Copy the main script
COPY src/compost.sh /app/compost.sh

# Make the script executable
RUN chmod +x /app/compost.sh

# Set the entrypoint to the script
ENTRYPOINT ["/app/compost.sh"]
