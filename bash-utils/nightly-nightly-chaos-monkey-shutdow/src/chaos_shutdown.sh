#!/bin/bash

set -euo pipefail

SERVICE_NAME="${1:-}"
FORCE_FLAG="${2:-}"

if [[ -z "$SERVICE_NAME" ]]; then
  echo "Error: Service name is required."
  exit 1
fi

if [[ "$FORCE_FLAG" == "--force" ]]; then
  echo "Forcefully stopping service: $SERVICE_NAME"
  sudo systemctl kill "$SERVICE_NAME" || echo "Failed to kill $SERVICE_NAME"
else
  echo "Gracefully stopping service: $SERVICE_NAME"
  sudo systemctl stop "$SERVICE_NAME" || echo "Failed to stop $SERVICE_NAME"
fi

echo "Shutdown simulation complete for $SERVICE_NAME"
