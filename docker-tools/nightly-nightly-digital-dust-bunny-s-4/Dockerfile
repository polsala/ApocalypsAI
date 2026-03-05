# Use a slim Python image for smaller size
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main script
COPY src/dust_bunny_sweeper.py .

# Define the entrypoint for the container
# This allows passing arguments directly to the Python script
ENTRYPOINT ["python", "dust_bunny_sweeper.py"]
