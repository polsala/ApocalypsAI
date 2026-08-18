#!/bin/bash
set -e

# This script acts as the entrypoint for the Docker container.
# It simply calls the Python script with the provided arguments.

# Ensure CHRONOSYNC_PASSWORD is set
if [ -z "$CHRONOSYNC_PASSWORD" ]; then
  echo "Error: CHRONOSYNC_PASSWORD environment variable must be set." >&2
  exit 1
fi

# Execute the Python script with all arguments
exec python3 /app/chronosync.py "$@"
