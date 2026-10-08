FROM python:3.9-slim-buster

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized utility to clean old files based on age."

WORKDIR /app

# Copy the Python script and the entrypoint script
COPY src/cleaner.py .
COPY src/entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint to our shell script
ENTRYPOINT ["./entrypoint.sh"]

# Default command if no arguments are provided (will show help)
CMD ["--help"]
