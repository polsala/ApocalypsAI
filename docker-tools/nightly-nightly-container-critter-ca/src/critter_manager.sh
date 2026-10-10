#!/bin/bash

set -euo pipefail

# Define base directories
CRITTER_DIR="critters"
CRITTER_TEMPLATE_DIR="src/critter_template"

# Ensure the critters directory exists
mkdir -p "$CRITTER_DIR"

# Function to initialize a new critter
init_critter() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: $0 init <critter_name>"
        exit 1
    fi

    local critter_path="$CRITTER_DIR/$name"
    if [ -d "$critter_path" ]; then
        echo "Error: Critter '$name' already exists." >&2
        exit 1
    fi

    mkdir -p "$critter_path"

    # Copy template files to the new critter's directory
    cp -r "$CRITTER_TEMPLATE_DIR/." "$critter_path/"

    # Create docker-compose.yml dynamically
    cat <<EOF > "$critter_path/docker-compose.yml"
version: '3.8'
services:
  ${name}-critter:
    build: .
    volumes:
      - ./mood.txt:/app/mood.txt # Persist mood
    container_name: ${name}-critter-container
EOF
    echo "Critter '$name' initialized."
}

# Function to start a critter container
start_critter() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: $0 start <critter_name>"
        exit 1
    fi
    local critter_path="$CRITTER_DIR/$name"
    if [ ! -d "$critter_path" ]; then
        echo "Error: Critter '$name' not found. Initialize it first." >&2
        exit 1
    fi
    echo "Starting ${name}-critter-container ..."
    docker-compose -f "$critter_path/docker-compose.yml" up -d
}

# Function to stop a critter container
stop_critter() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: $0 stop <critter_name>"
        exit 1
    fi
    local critter_path="$CRITTER_DIR/$name"
    if [ ! -d "$critter_path" ]; then
        echo "Error: Critter '$name' not found." >&2
        exit 1
    }
    echo "Stopping ${name}-critter-container ..."
    docker-compose -f "$critter_path/docker-compose.yml" down
}

# Function to get critter status
status_critter() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: $0 status <critter_name>"
        exit 1
    }
    local critter_path="$CRITTER_DIR/$name"
    if [ ! -d "$critter_path" ]; then
        echo "Error: Critter '$name' not found." >&2
        exit 1
    }
    docker-compose -f "$critter_path/docker-compose.yml" ps
}

# Function to interact with a critter
interact_critter() {
    local name="$1"
    local command="$2"
    local critter_path="$CRITTER_DIR/$name"

    if [ ! -d "$critter_path" ]; then
        echo "Error: Critter '$name' not found. Initialize it first." >&2
        exit 1
    fi

    # Check if the container is running before attempting to exec
    local container_name="${name}-critter-container"
    if ! docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        echo "Error: Critter '$name' container is not running. Please start it first." >&2
        exit 1
    fi

    if [ -z "$command" ]; then
        # No command, just get current mood
        docker-compose -f "$critter_path/docker-compose.yml" exec "${name}-critter" python /app/critter.py
    else
        # Send specific command
        docker-compose -f "$critter_path/docker-compose.yml" exec "${name}-critter" python /app/critter.py "$command"
    fi
}

# Main script logic
case "$1" in
    init)
        init_critter "$2"
        ;;
    start)
        start_critter "$2"
        ;;
    stop)
        stop_critter "$2"
        ;;
    status)
        status_critter "$2"
        ;;
    interact)
        interact_critter "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {init|start|stop|status|interact} <critter_name> [command]"
        exit 1
        ;;
esac
