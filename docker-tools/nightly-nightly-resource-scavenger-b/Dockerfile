FROM python:3.9-slim-buster

WORKDIR /app

# Copy the source files
COPY src/ .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]
