#!/bin/bash

# nightly-bash-env-sync
# A bash script to synchronize environment variables from a source file to the current shell session.

# Check if a source file argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <source_env_file>"
  exit 1
fi

SOURCE_FILE="$1"

# Check if the source file exists and is readable
if [ ! -f "$SOURCE_FILE" ] || [ ! -r "$SOURCE_FILE" ]; then
  echo "Error: Source file '$SOURCE_FILE' not found or not readable."
  exit 1
fi

# Source the file to export variables into the current shell
# The 'source' command (or '.') executes commands from a file in the current shell.
# This is crucial for the exported variables to affect the parent shell.
source "$SOURCE_FILE"

echo "Environment variables from '$SOURCE_FILE' have been synchronized."

exit 0
