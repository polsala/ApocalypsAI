FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator Agent"

# Install Docker CLI
RUN apk add --no-cache docker-cli bash

# Copy the main script
COPY src/compost_bin.sh /usr/local/bin/compost_bin.sh

# Make the script executable
RUN chmod +x /usr/local/bin/compost_bin.sh

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/compost_bin.sh"]
