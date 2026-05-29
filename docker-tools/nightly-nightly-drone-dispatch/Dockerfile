# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/drone_dispatcher.py .

# Run the Python script when the container launches
CMD ["python", "drone_dispatcher.py"]
