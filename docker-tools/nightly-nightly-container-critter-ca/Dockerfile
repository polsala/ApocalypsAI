FROM docker:latest

LABEL maintainer="ApocalypsAI Integrator Agent"
LABEL description="A containerized utility to monitor, refresh, and prune your Docker 'pet' containers."

WORKDIR /app

# Copy the care script
COPY src/care_script.sh /app/care_script.sh

# Make the script executable
RUN chmod +x /app/care_script.sh

# Set the entrypoint to the script
ENTRYPOINT ["/app/care_script.sh"]
