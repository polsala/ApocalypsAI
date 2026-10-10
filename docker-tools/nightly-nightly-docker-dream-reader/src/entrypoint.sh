#!/bin/bash
# This script serves as the entrypoint for the Docker container.
# It simply executes the Python dream reader script with the provided arguments.

# Ensure Python script is executable (though it's run via python interpreter)
chmod +x /app/src/dream_reader.py

# Execute the Python script with all arguments passed to the Docker container
exec python /app/src/dream_reader.py "$@"
