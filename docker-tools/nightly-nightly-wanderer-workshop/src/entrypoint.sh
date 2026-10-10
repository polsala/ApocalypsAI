#!/bin/bash

# This script acts as the entrypoint for the wanderer-workshop container.
# It allows for flexible usage:
# - If the command is "http-server", it starts a Python HTTP server.
# - Otherwise, it executes the provided command.

set -e

if [ "$1" = "http-server" ]; then
    echo "Starting Python HTTP server on port 8000..."
    # Ensure the current directory is writable for the server to list files
    # and for potential file uploads if a more advanced server was used.
    # For http.server, it just needs read access to serve.
    python3 -m http.server 8000
else
    # Execute the command passed to docker run
    exec "$@"
fi
