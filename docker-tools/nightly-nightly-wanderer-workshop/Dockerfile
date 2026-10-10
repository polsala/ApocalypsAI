# Use a lightweight base image
FROM alpine:3.18

# Set labels for better identification
LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A portable development workshop for wasteland wanderers."

# Install essential packages
# bash for better shell scripting, python3 for general scripting and http.server
# nano/vim for basic text editing, curl for network requests, jq for JSON processing
RUN apk add --no-cache \
    bash \
    python3 \
    py3-pip \
    nano \
    vim \
    curl \
    jq

# Set the working directory inside the container
WORKDIR /app

# Copy the custom entrypoint script
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the default port for the HTTP server
EXPOSE 8000

# Set the entrypoint to our custom script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command if none is provided (starts the HTTP server)
CMD ["http-server"]
