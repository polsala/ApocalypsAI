FROM alpine:latest

# Install docker-cli to interact with the Docker daemon
RUN apk add --no-cache docker-cli

WORKDIR /app

# Copy the cleaner script into the container
COPY src/cleaner.sh .

# Make the script executable
RUN chmod +x cleaner.sh

# Set the entrypoint to run the cleaner script
ENTRYPOINT ["./cleaner.sh"]
