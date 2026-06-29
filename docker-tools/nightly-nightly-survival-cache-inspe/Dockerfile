FROM alpine:3.18

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="Containerized utility to safely inspect archive contents and SHA256 sum."

# Install necessary tools
RUN apk add --no-cache tar unzip coreutils

# Copy the inspection script
COPY src/inspect_cache.sh /usr/local/bin/inspect_cache.sh

# Make the script executable
RUN chmod +x /usr/local/bin/inspect_cache.sh

# Set the entrypoint to our script
ENTRYPOINT ["/usr/local/bin/inspect_cache.sh"]

CMD ["--help"]
