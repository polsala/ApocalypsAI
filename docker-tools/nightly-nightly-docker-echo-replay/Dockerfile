# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the main script
COPY src/echo_replay.py .

# Install pytest for testing purposes (only needed for running tests inside the container)
# In a production scenario, this might be omitted or handled in a multi-stage build.
RUN pip install pytest

# Set the entrypoint for the application
# This allows running commands like: docker run nightly-docker-echo-replay record ...
ENTRYPOINT ["python", "echo_replay.py"]
