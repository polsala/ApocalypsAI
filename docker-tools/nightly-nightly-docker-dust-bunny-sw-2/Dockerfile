# Use a minimal base image with bash and docker client
FROM alpine/git:latest

# Install Docker CLI (alpine's docker package includes the client)
RUN apk add --no-cache docker

# Copy the sweeper script into the container
COPY src/dust_bunny_sweeper.sh /usr/local/bin/dust_bunny_sweeper.sh

# Make the script executable
RUN chmod +x /usr/local/bin/dust_bunny_sweeper.sh

# Set the entrypoint to run the sweeper script
ENTRYPOINT ["/usr/local/bin/dust_bunny_sweeper.sh"]
