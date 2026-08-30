#!/bin/bash

# Ensure required environment variables are set
if [ -z "$SOURCE_DIR" ] || [ -z "$DEST_DIR" ] || [ -z "$ENCRYPTION_KEY" ]; then
  echo "Error: SOURCE_DIR, DEST_DIR, and ENCRYPTION_KEY must be set."
  exit 1
fi

# Execute the Python application
exec python /app/app.py
