# Use a lightweight base image with Python and yamllint installed
FROM python:3.11-slim

# Install yamllint
RUN pip install --no-cache-dir yamllint

# Copy the action script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]
