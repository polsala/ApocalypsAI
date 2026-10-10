# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install the Docker SDK for Python
# This allows the script to interact with the Docker daemon
RUN pip install docker

# Copy the Python script into the container
COPY src/monitor.py /app/monitor.py

# Set the entrypoint for the container
# This command will be executed when the container starts
ENTRYPOINT ["python", "/app/monitor.py"]
