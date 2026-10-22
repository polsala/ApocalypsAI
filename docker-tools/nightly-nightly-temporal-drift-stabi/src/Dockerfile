FROM alpine:latest

# Install ntpdate for time synchronization
RUN apk add --no-cache ntp

WORKDIR /app

# Copy the stabilization script
COPY stabilize.sh .

# Make the script executable
RUN chmod +x stabilize.sh

# Set the script as the entrypoint
ENTRYPOINT ["./stabilize.sh"]
