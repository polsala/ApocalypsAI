FROM alpine:latest

# Install bash and docker-cli
RUN apk add --no-cache bash docker-cli

# Copy the feeder script into the container
COPY src/feeder.sh /usr/local/bin/feeder.sh

# Make the script executable
RUN chmod +x /usr/local/bin/feeder.sh

# Set the entrypoint to run the feeder script
ENTRYPOINT ["/usr/local/bin/feeder.sh"]
