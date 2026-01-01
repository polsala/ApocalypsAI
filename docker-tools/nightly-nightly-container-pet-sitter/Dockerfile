FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install Docker CLI
# We use the official Docker client for Alpine, which is lightweight.
RUN apk add --no-cache docker-cli

# Copy the pet sitter script
COPY src/pet_sitter.sh /usr/local/bin/pet_sitter.sh

# Make the script executable
RUN chmod +x /usr/local/bin/pet_sitter.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/usr/local/bin/pet_sitter.sh"]
