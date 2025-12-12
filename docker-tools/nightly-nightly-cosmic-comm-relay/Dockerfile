# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/
COPY tests/ /app/tests/

# Install any needed packages specified in requirements.txt
# (We don't have one for this simple script, but it's good practice)
# RUN pip install --no-cache-dir -r requirements.txt

# Install pytest for running tests
RUN pip install --no-cache-dir pytest

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
# ENV NAME World

# Run relay.py when the container launches
CMD ["python", "relay.py"]
