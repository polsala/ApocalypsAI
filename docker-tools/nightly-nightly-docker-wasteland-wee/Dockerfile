FROM alpine:latest

# Install bash, as it's used by the weeder.sh script
RUN apk add --no-cache bash

WORKDIR /app

# Copy the main script into the container
COPY src/weeder.sh .

# Make the script executable
RUN chmod +x weeder.sh

# Set the entrypoint to run the script
ENTRYPOINT ["bash", "./weeder.sh"]

# Default command to show help if no arguments are provided
CMD ["--help"]
