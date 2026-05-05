FROM docker:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"

WORKDIR /app

# Copy the entrypoint script and the test script
COPY src/entrypoint.sh /app/entrypoint.sh
COPY tests/test_entrypoint.sh /app/tests/test_entrypoint.sh

# Make them executable
RUN chmod +x /app/entrypoint.sh /app/tests/test_entrypoint.sh

# Set the entrypoint for the utility
ENTRYPOINT ["/app/entrypoint.sh"]
