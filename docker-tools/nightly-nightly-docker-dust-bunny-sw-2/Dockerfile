# Use a minimal base image
FROM alpine:latest

# Install docker client (needed to interact with host docker daemon)
# This assumes the host's docker socket is mounted.
RUN apk add --no-cache docker

# Copy the sweeper script into the container
COPY src/dust_bunny_sweeper.sh /usr/local/bin/dust_bunny_sweeper.sh
RUN chmod +x /usr/local/bin/dust_bunny_sweeper.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/usr/local/bin/dust_bunny_sweeper.sh"]
