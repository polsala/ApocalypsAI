FROM alpine:3.18

LABEL maintainer="ApocalypsAI Integrator"
LABEL description="A Dockerized environment for testing time-sensitive applications using libfaketime."

# Install necessary packages: bash for the entrypoint, libfaketime for time manipulation
RUN apk add --no-cache bash faketime

# Copy the entrypoint script into the container
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint to our script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command if none is provided (e.g., just run 'date')
CMD ["date"]
