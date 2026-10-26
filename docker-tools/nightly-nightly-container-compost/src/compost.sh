#!/bin/bash

# Nightly Container Compost - Core Script

# Default Docker command. Can be overridden for testing.
docker_cmd="docker"

# Default settings
DRY_RUN=false
CONTAINER_AGE_HOURS=24
PRUNE_CONTAINERS=true
PRUNE_IMAGES=true
PRUNE_VOLUMES=true
PRUNE_BUILD_CACHE=true

# Function to display usage
usage() {
  echo "Usage: compost.sh [--dry-run] [--container-age-hours <hours>] [--no-prune-containers] [--no-prune-images] [--no-prune-volumes] [--no-prune-build-cache]"
  echo ""
  echo "  --dry-run:               Perform a dry run. No items will be removed, only reported."
  echo "  --container-age-hours:   Minimum age in hours for stopped containers to be considered stale. Default: ${CONTAINER_AGE_HOURS}"
  echo "  --no-prune-containers:   Skip pruning of stale containers."
  echo "  --no-prune-images:       Skip pruning of dangling images."
  echo "  --no-prune-volumes:      Skip pruning of dangling volumes."
  echo "  --no-prune-build-cache:  Skip pruning of build cache."
  exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  key="$1"
  case $key in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --container-age-hours)
      CONTAINER_AGE_HOURS="$2"
      shift 2
      ;;
    --no-prune-containers)
      PRUNE_CONTAINERS=false
      shift
      ;;
    --no-prune-images)
      PRUNE_IMAGES=false
      shift
      ;;
    --no-prune-volumes)
      PRUNE_VOLUMES=false
      shift
      ;;
    --no-prune-build-cache)
      PRUNE_BUILD_CACHE=false
      shift
      ;;
    *)
      usage
      ;;
  esac
done

# --- Reporting Functions ---

report_stale_containers() {
  echo "\n--- Stale Exited Containers (older than ${CONTAINER_AGE_HOURS} hours) ---"
  local containers=$(${docker_cmd} ps -aq --filter "status=exited" --filter "until=${CONTAINER_AGE_HOURS}h")
  if [ -z "$containers" ]; then
    echo "No stale exited containers found."
  else
    ${docker_cmd} ps -a --filter "status=exited" --filter "until=${CONTAINER_AGE_HOURS}h" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
  fi
  echo ""
}

report_dangling_images() {
  echo "\n--- Dangling Images ---"
  local images=$(${docker_cmd} images -f "dangling=true" -q)
  if [ -z "$images" ]; then
    echo "No dangling images found."
  else
    ${docker_cmd} images -f "dangling=true" --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
  fi
  echo ""
}

report_dangling_volumes() {
  echo "\n--- Dangling Volumes ---"
  local volumes=$(${docker_cmd} volume ls -f "dangling=true" -q)
  if [ -z "$volumes" ]; then
    echo "No dangling volumes found."
  else
    ${docker_cmd} volume ls -f "dangling=true" --format "table {{.Name}}\t{{.Driver}}"
  fi
  echo ""
}

report_build_cache() {
  echo "\n--- Docker Build Cache (potential for cleanup) ---"
  # docker builder prune -f doesn't have a dry-run report, so we just indicate it will be pruned.
  # We can't list specific items without actually pruning or using complex internal commands.
  echo "Build cache will be pruned if not in dry-run mode."
  echo ""
}

# --- Pruning Functions ---

prune_stale_containers() {
  if $PRUNE_CONTAINERS; then
    echo "Composting stale exited containers..."
    if $DRY_RUN; then
      echo "(Dry run) Would run: ${docker_cmd} container prune -f --filter \"until=${CONTAINER_AGE_HOURS}h\""
    else
      ${docker_cmd} container prune -f --filter "until=${CONTAINER_AGE_HOURS}h"
    fi
  else
    echo "Skipping stale container composting."
  fi
}

prune_dangling_images() {
  if $PRUNE_IMAGES; then
    echo "Composting dangling images..."
    if $DRY_RUN; then
      echo "(Dry run) Would run: ${docker_cmd} image prune -f"
    else
      ${docker_cmd} image prune -f
    fi
  else
    echo "Skipping dangling image composting."
  fi
}

prune_dangling_volumes() {
  if $PRUNE_VOLUMES; then
    echo "Composting dangling volumes..."
    if $DRY_RUN; then
      echo "(Dry run) Would run: ${docker_cmd} volume prune -f"
    else
      ${docker_cmd} volume prune -f
    fi
  else
    echo "Skipping dangling volume composting."
  fi
}

prune_build_cache() {
  if $PRUNE_BUILD_CACHE; then
    echo "Composting Docker build cache..."
    if $DRY_RUN; then
      echo "(Dry run) Would run: ${docker_cmd} builder prune -f"
    else
      ${docker_cmd} builder prune -f
    fi
  else
    echo "Skipping build cache composting."
  fi
}

# --- Main Logic ---

echo "Nightly Container Compost Heap is running..."

if $DRY_RUN; then
  echo "*** DRY RUN MODE ENABLED *** No changes will be made to your Docker environment."
else
  echo "*** LIVE COMPOSTING MODE *** Changes will be made to your Docker environment."
fi

report_stale_containers
report_dangling_images
report_dangling_volumes
report_build_cache

if $DRY_RUN; then
  echo "\nDry run complete. To apply changes, run without --dry-run."
else
  echo "\nInitiating composting process..."
  prune_stale_containers
  prune_dangling_images
  prune_dangling_volumes
  prune_build_cache
  echo "\nComposting process complete."
fi
