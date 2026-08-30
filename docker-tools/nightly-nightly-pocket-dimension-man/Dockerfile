FROM alpine/git:latest

# Install Docker CLI and bash
RUN apk add --no-cache docker-cli bash

# Set the working directory
WORKDIR /app

# Copy the main script
COPY src/pocket_dimension.sh /usr/local/bin/pocket-dimension-manager

# Make the script executable
RUN chmod +x /usr/local/bin/pocket-dimension-manager

# Set the entrypoint to our script
ENTRYPOINT ["pocket-dimension-manager"]
CMD ["--help"]
