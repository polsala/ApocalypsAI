# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/

# Install any needed packages specified in requirements.txt
# (Assuming docker SDK is installed via pip)
RUN pip install --no-cache-dir docker

# Make port 80 available to the world outside this container
# (Not strictly necessary for this CLI tool, but good practice for containerized apps)
# EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
