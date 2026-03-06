#!/bin/bash

# Function to check if a command exists
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

# Check for Docker client availability
if ! command_exists docker; then
  echo "Error: Docker client not found. Please ensure Docker is installed and in your PATH."
  exit 1
fi

# Parse arguments
PRUNE_MODE=false
for arg in "$@"; do
  case $arg in
    --prune|--force)
      PRUNE_MODE=true
      shift # Remove argument from processing
      ;;
    *)
      # Unknown argument, ignore for now or handle as error
      ;;
  esac
done

if [ "$PRUNE_MODE" = true ]; then
  echo "✂️ Time to get pruning! Clearing out the digital weeds from your container garden.\n"
  # Perform the actual pruning
  # docker system prune -a -f would remove all unused images, not just dangling ones.
  # For a "tidy-upper", we'll stick to the default system prune which is safer.
  # It removes: all stopped containers, all networks not used by at least one container,
  # all dangling images, and all dangling build cache.
  # It does NOT remove: images not associated with a container, or volumes not associated with a container.
  # For volumes, we explicitly prune dangling ones.
  
  # Run system prune first
  docker system prune -f
  
  # Explicitly prune dangling volumes, as system prune doesn't always catch all of them
  # (e.g., if they were created without a container and never used).
  docker volume prune -f
  
  echo "\n✨ Your container garden is now sparkling clean! Happy cultivating!"
else
  echo "🌿 Greetings, Digital Gardener! Time to inspect your container garden for any unruly digital weeds.\n"
  echo "🔍 Found these potential weeds:\n"

  echo "--- Dangling Images (forgotten seeds) ---"
  docker images -f dangling=true --format "{{.Repository}}:{{.Tag}} ({{.Size}})" || echo "<none>"
  echo "\n--- Exited Containers (withered blossoms) ---"
  docker ps -a -f status=exited --format "{{.Names}} ({{.Status}})" || echo "<none>"
  echo "\n--- Dangling Volumes (unclaimed soil plots) ---"
  docker volume ls -f dangling=true --format "{{.Name}}" || echo "<none>"
  echo "\n--- Unused Networks (tangled roots) ---"
  docker network ls -f dangling=true --format "{{.Name}}" || echo "<none>"

  echo "\n🌱 Your garden looks remarkably tidy! No major pruning needed at this moment."
  echo "\nTo perform actual pruning, run with the '--prune' flag."
fi
