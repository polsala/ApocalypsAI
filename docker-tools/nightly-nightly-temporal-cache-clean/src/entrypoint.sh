#!/bin/bash

# This script acts as the entrypoint for the Docker container.
# It simply passes all command-line arguments directly to the Python cleaner script.

# Execute the Python script with all arguments
python /app/cleaner.py "$@"
