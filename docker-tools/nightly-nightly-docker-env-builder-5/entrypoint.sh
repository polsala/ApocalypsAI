#!/bin/bash

set -euo pipefail

CONFIG_FILE="env.yaml"

# Parse command-line arguments for config file
while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    --config)
      CONFIG_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      shift # past argument
      ;;
  esac
done

# Check if config file exists and is readable
if [ ! -f "$CONFIG_FILE" ] || [ ! -r "$CONFIG_FILE" ]; then
  echo "Error: Configuration file '$CONFIG_FILE' not found or not readable."
  exit 1
fi

# Install packages
echo "Installing packages..."
PACKAGES=$(yq e '.packages[]' "$CONFIG_FILE")
if [ -n "$PACKAGES" ]; then
  apt-get update && apt-get install -y --no-install-recommends $PACKAGES \
    && rm -rf /var/lib/apt/lists/*
fi

# Install tools (e.g., Node.js, Docker Compose)
echo "Installing tools..."
TOOLS=$(yq e '.tools[]' "$CONFIG_FILE")
if [ -n "$TOOLS" ]; then
  while IFS= read -r tool_line; do
    TOOL_NAME=$(echo "$tool_line" | yq e '.name' -)
    TOOL_VERSION=$(yq e '.version' -)

    echo "Installing $TOOL_NAME (version: $TOOL_VERSION)..."

    case "$TOOL_NAME" in
      "nodejs")
        if [ "$TOOL_VERSION" == "latest" ]; then
          # Install latest stable Node.js
          curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
          apt-get install -y nodejs
        else
          # Install specific version
          curl -fsSL https://deb.nodesource.com/setup_$TOOL_VERSION.x | bash -
          apt-get install -y nodejs
        fi
        ;; 
      "docker-compose")
        if [ "$TOOL_VERSION" == "latest" ]; then
          LATEST_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r '.tag_name')
          LATEST_COMPOSE_VERSION=${LATEST_COMPOSE_VERSION#v}
          curl -L "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
        else
          curl -L "https://github.com/docker/compose/releases/download/v${TOOL_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
        fi
        ;; 
      *)
        echo "Warning: Unknown tool '$TOOL_NAME'. Skipping."
        ;;
    esac
  done <<< "$TOOLS"
fi

# Set up port mappings (for informational purposes, Docker handles actual mapping)
echo "Setting up port mappings..."
PORTS=$(yq e '.ports[]' "$CONFIG_FILE")
if [ -n "$PORTS" ]; then
  echo "Port mappings configured: $PORTS"
fi

# Set up volume mounts (for informational purposes, Docker handles actual mounting)
echo "Setting up volume mounts..."
VOLUMES=$(yq e '.volumes[]' "$CONFIG_FILE")
if [ -n "$VOLUMES" ]; then
  echo "Volume mounts configured: $VOLUMES"
fi

echo "Environment setup complete! You are now inside the container for '$CONFIG_FILE'."

# Keep the container running
exec tail -f /dev/null
