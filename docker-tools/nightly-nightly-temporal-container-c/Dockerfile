FROM alpine:latest

# Install bash and docker-cli
RUN apk add --no-cache bash docker-cli

WORKDIR /app

# Copy the monitoring script into the container
COPY src/monitor.sh /app/monitor.sh

# Make the script executable
RUN chmod +x /app/monitor.sh

# Set the entrypoint to run the monitoring script
ENTRYPOINT ["/app/monitor.sh"]
