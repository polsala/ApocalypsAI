#!/bin/bash

# Nightly Chrono-Container Courier (NCCC)
# Orchestrates Docker to run commands in specified container environments.

set -euo pipefail

# --- Configuration Defaults ---
DEFAULT_CONFIG_FILE="config.json"
DEFAULT_OUTPUT_FILE="chrono_courier_results.log"
DEFAULT_MOUNT_PATH="/app"

# --- Functions ---

# Usage information
usage() {
    echo "Usage: $0 [config_file.json]"
    echo "Runs commands in a Docker container as specified by the config file."
    echo "If no config_file.json is provided, it defaults to '$DEFAULT_CONFIG_FILE' in the current directory."
    exit 1
}

# Check for prerequisites
check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        echo "Error: Docker is not installed or not in PATH." >&2
        echo "Please install Docker to use the Chrono-Container Courier." >&2
        exit 1
    fi
    if ! command -v jq &> /dev/null; then
        echo "Error: 'jq' is not installed or not in PATH." >&2
        echo "Please install 'jq' (e.g., 'sudo apt-get install jq') to parse the config file." >&2
        exit 1
    fi
}

# Parse config file
parse_config() {
    local config_file="$1"

    if [[ ! -f "$config_file" ]]; then
        echo "Error: Configuration file '$config_file' not found." >&2
        usage
    fi

    IMAGE=$(jq -r '.image' "$config_file")
    COMMANDS_ARRAY=($(jq -r '.commands[]' "$config_file"))
    OUTPUT_FILE=$(jq -r ".output_file // \"$DEFAULT_OUTPUT_FILE\"" "$config_file")
    MOUNT_PATH=$(jq -r ".mount_path // \"$DEFAULT_MOUNT_PATH\"" "$config_file")

    if [[ -z "$IMAGE" || ${#COMMANDS_ARRAY[@]} -eq 0 ]]; then
        echo "Error: 'image' and 'commands' fields are required in '$config_file'." >&2
        exit 1
    fi

    # Construct a single command string for Docker
    FULL_COMMAND_STRING=""
    for cmd in "${COMMANDS_ARRAY[@]}"; do
        FULL_COMMAND_STRING+="$cmd && "
    done
    FULL_COMMAND_STRING="${FULL_COMMAND_STRING% && }" # Remove trailing ' && '

    # Escape single quotes within the command string for bash -c
    FULL_COMMAND_STRING_ESCAPED=$(echo "$FULL_COMMAND_STRING" | sed "s/'/'\\''/g")
}

# --- Main Execution ---

check_prerequisites

CONFIG_FILE="${1:-$DEFAULT_CONFIG_FILE}"
parse_config "$CONFIG_FILE"

echo "--- Chrono-Container Courier Dispatch ---"
echo "Target Image: $IMAGE"
echo "Commands to run: ${COMMANDS_ARRAY[@]}"
echo "Output will be saved to: $OUTPUT_FILE"
echo "Mounting host directory '$(pwd)' to container path '$MOUNT_PATH'"
echo "-----------------------------------------"

# Pull the Docker image
echo "Pulling Docker image '$IMAGE'..."
if ! docker pull "$IMAGE"; then
    echo "Error: Failed to pull Docker image '$IMAGE'." >&2
    exit 1
fi

# Run the commands in the container
echo "Running commands in container..."

# Use a temporary file for output capture to ensure both stdout and stderr are caught
TEMP_OUTPUT=$(mktemp)
TEMP_EXIT_CODE=$(mktemp)

# Execute the docker run command, capturing stdout/stderr and exit code
# We use /bin/sh -c to ensure the commands are executed as a single string
# and allow for shell features like '&&'
# The host's current directory is mounted into the container at $MOUNT_PATH

# Mock rationale: The actual docker run command is complex and interacts with the host's Docker daemon.
# For testing, this command will be mocked to simulate its behavior without actual container execution.
# The mock will capture the arguments passed to docker run and simulate output/exit codes.

if docker run --rm \
             -v "$(pwd):$MOUNT_PATH" \
             "$IMAGE" \
             /bin/sh -c "$FULL_COMMAND_STRING_ESCAPED" \
             > "$TEMP_OUTPUT" 2>&1; then
    CONTAINER_EXIT_CODE=0
else
    CONTAINER_EXIT_CODE=$?
fi

# Save the exit code
echo "$CONTAINER_EXIT_CODE" > "$TEMP_EXIT_CODE"

echo "-----------------------------------------"
echo "Container execution finished. Exit code: $(cat "$TEMP_EXIT_CODE")"

# Write captured output to the specified file
cat "$TEMP_OUTPUT" > "$OUTPUT_FILE"

echo "Full output saved to '$OUTPUT_FILE'."

# Clean up temporary files
rm "$TEMP_OUTPUT" "$TEMP_EXIT_CODE"

exit "$CONTAINER_EXIT_CODE"
