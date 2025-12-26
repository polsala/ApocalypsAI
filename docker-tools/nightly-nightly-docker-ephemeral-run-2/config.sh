#!/bin/bash

# GitHub Actions Runner Configuration
# This script configures the runner for ephemeral use

set -e

# Default values
RUNNER_URL=""
RUNNER_TOKEN=""
RUNNER_NAME=""
RUNNER_REPLACE=false
RUNNER_EPHEMERAL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            RUNNER_URL="$2"
            shift 2
            ;;
        --token)
            RUNNER_TOKEN="$2"
            shift 2
            ;;
        --name)
            RUNNER_NAME="$2"
            shift 2
            ;;
        --unattended)
            RUNNER_UNATTENDED=true
            shift
            ;;
        --replace)
            RUNNER_REPLACE=true
            shift
            ;;
        --ephemeral)
            RUNNER_EPHEMERAL=true
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$RUNNER_URL" ] || [ -z "$RUNNER_TOKEN" ] || [ -z "$RUNNER_NAME" ]; then
    echo "Usage: $0 --url <url> --token <token> --name <name> [--unattended] [--replace] [--ephemeral]"
    exit 1
fi

# Configuration file path
CONFIG_FILE=".runner"

# Remove existing configuration if replace is enabled
if [ "$RUNNER_REPLACE" = true ] && [ -f "$CONFIG_FILE" ]; then
    echo "Removing existing runner configuration..."
    ./config.sh remove --token "$RUNNER_TOKEN" --unattended || true
fi

# Create configuration
echo "Configuring runner..."

# Set up environment
export RUNNER_ALLOW_RUNASROOT=1

# Run configuration
./bin/Runner.Listener configure \
    --url "$RUNNER_URL" \
    --token "$RUNNER_TOKEN" \
    --name "$RUNNER_NAME" \
    --work "_work" \
    --replace \
    ${RUNNER_EPHEMERAL:+--ephemeral}

if [ $? -eq 0 ]; then
    echo "Runner configured successfully"
else
    echo "Failed to configure runner"
    exit 1
fi
