FROM alpine:3.18

# Install Docker CLI
# We need the docker client inside the container to interact with the host's daemon.
RUN apk add --no-cache docker-cli bash

# Set the working directory
WORKDIR /app

# Copy the sweeper script
COPY src/dust_bunny_sweeper.sh /app/dust_bunny_sweeper.sh

# Make the script executable
RUN chmod +x /app/dust_bunny_sweeper.sh

# Define the entrypoint
ENTRYPOINT ["/app/dust_bunny_sweeper.sh"]
