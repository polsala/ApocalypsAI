# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# (For this simple app, we'll just install Flask directly)
RUN pip install Flask

# Copy the current directory contents into the container at /app
COPY src/app.py .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
