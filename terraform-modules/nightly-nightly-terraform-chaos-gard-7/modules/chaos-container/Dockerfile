# Chaos Container Dockerfile
# A whimsical container for introducing chaos into your infrastructure

FROM alpine:latest

# Install necessary tools for chaos
RUN apk add --no-cache \
    curl \
    iperf3 \
    stress-ng \
    tc \
    python3 \
    py3-pip

# Install chaos tools
RUN pip3 install --no-cache-dir \
    chaospy \
    locust

# Create chaos scripts directory
RUN mkdir -p /opt/chaos

# Copy chaos scripts
COPY chaos-scripts/ /opt/chaos/

# Make scripts executable
RUN chmod +x /opt/chaos/*.sh
RUN chmod +x /opt/chaos/*.py

# Set working directory
WORKDIR /opt/chaos

# Default command - run chaos orchestrator
CMD ["python3", "chaos_orchestrator.py"]

# Expose health check endpoint
EXPOSE 8080
