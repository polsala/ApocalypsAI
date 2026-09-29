# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# (For this simple app, we'll install directly)
RUN pip install --no-cache-dir docker

# Copy the current directory contents into the container at /app
COPY src/app.py .

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
