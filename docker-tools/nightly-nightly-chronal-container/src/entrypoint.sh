#!/bin/bash
# Nightly Chronal Container - Entrypoint Script

# This script simply executes the command passed to the Docker container.
# It allows the user to run any command within the defined "past" environment.

# Execute the command with all arguments
exec "$@"
