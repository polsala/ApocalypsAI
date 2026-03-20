# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY src/ .

# Expose port 8080 for the Flask app
EXPOSE 8080

# Run the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
