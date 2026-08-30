#!/bin/bash
set -euo pipefail

# The path to the docker-compose file. Defaults to /app/docker-compose.yml inside the container.
# Can be overridden by setting OASIS_COMPOSE_FILE environment variable for testing or custom setups.
COMPOSE_FILE="${OASIS_COMPOSE_FILE:-/app/docker-compose.yml}"

case "$1" in
    up)
        echo "Cultivating your Ephemeral Dev Oasis..."
        docker compose -f "$COMPOSE_FILE" up -d
        echo "Oasis is blooming! Access services via host ports."
        ;;
    down)
        echo "Wilting your Ephemeral Dev Oasis..."
        docker compose -f "$COMPOSE_FILE" down
        echo "Oasis has returned to the sands."
        ;;
    status)
        echo "Checking the vitality of your Ephemeral Dev Oasis..."
        docker compose -f "$COMPOSE_FILE" ps
        ;;
    *)
        echo "Usage: $0 {up|down|status}"
        echo "  up     - Cultivate (start) the dev oasis."
        echo "  down   - Wilt (stop and remove) the dev oasis."
        echo "  status - Check the vitality (status) of the dev oasis."
        exit 1
        ;;
esac
