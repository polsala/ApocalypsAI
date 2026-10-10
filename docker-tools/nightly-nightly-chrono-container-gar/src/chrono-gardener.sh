#!/bin/bash

set -euo pipefail

COMPOSE_FILE=""
DURATION=0
PROJECT_NAME=""

# Function to display usage information
usage() {
    echo "Usage: $0 --compose-file <path> --duration <minutes> [--project-name <name>]"
    echo "  --compose-file <path> : Path to your docker-compose.yml file."
    echo "  --duration <minutes>  : The number of minutes the environment should run."
    echo "  --project-name <name> : Optional. Custom project name for Docker Compose."
    exit 1
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --compose-file)
        COMPOSE_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        --duration)
        DURATION="$2"
        shift # past argument
        shift # past value
        ;;
        --project-name)
        PROJECT_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        *)
        usage # unknown option
        ;;
    esac
done

# Validate required arguments
if [[ -z "$COMPOSE_FILE" || "$DURATION" -le 0 ]]; then
    echo "Error: --compose-file and a positive --duration are required."
    usage
fi

if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo "Error: Docker Compose file not found at '$COMPOSE_FILE'."
    exit 1
fi

# Determine project name if not provided
if [[ -z "$PROJECT_NAME" ]]; then
    # Use the directory name of the compose file as a default project name
    PROJECT_NAME="$(basename "$(dirname "$COMPOSE_FILE")")-$(date +%s)"
    echo "No project name provided. Using generated name: $PROJECT_NAME"
fi

# --- Chrono-Container Gardener Operations ---

echo "\n🌱 Planting your Chrono-Container Garden (Project: $PROJECT_NAME)..."

# Start containers in detached mode
if ! docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d; then
    echo "❌ Failed to plant the garden. Check your Docker Compose file and Docker daemon."
    exit 1
fi

echo "✅ Garden planted successfully! Nurturing your sprouts for $DURATION minutes..."

# Wait for the specified duration
sleep_seconds=$((DURATION * 60))
sleep "$sleep_seconds"

echo "\n✂️ Harvesting and pruning your Chrono-Container Garden..."

# Stop and remove containers, networks, and volumes defined in the compose file
if ! docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down; then
    echo "⚠️ Failed to prune the garden. Manual cleanup might be required for project '$PROJECT_NAME'."
    exit 1
fi

echo "✅ Garden successfully pruned. Ready for new seeds!"
