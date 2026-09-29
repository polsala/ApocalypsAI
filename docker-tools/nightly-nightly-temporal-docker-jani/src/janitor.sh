#!/bin/sh

echo "Temporal Anomaly Detected! Initiating Chrono-Purge Protocol..."
echo "Scanning for temporal residue and unused dimensional constructs..."

# Default to true for containers and dangling images, unless explicitly set to 'false'
PRUNE_CONTAINERS=${DOCKER_PRUNE_CONTAINERS:-true}
PRUNE_IMAGES=${DOCKER_PRUNE_IMAGES:-true}

# Default to false for volumes, networks, and all images, unless explicitly set to 'true'
PRUNE_VOLUMES=${DOCKER_PRUNE_VOLUMES:-false}
PRUNE_NETWORKS=${DOCKER_PRUNE_NETWORKS:-false}
PRUNE_ALL_IMAGES=${DOCKER_PRUNE_ALL_IMAGES:-false}

# Force removal without prompt
FORCE_FLAG="-f"

echo "Chrono-Purge Configuration:"
echo "  Containers: ${PRUNE_CONTAINERS}"
echo "  Images (dangling): ${PRUNE_IMAGES}"
echo "  Images (all unused): ${PRUNE_ALL_IMAGES}"
echo "  Volumes:    ${PRUNE_VOLUMES}"
echo "  Networks:   ${PRUNE_NETWORKS}"

echo ""

if [ "$PRUNE_CONTAINERS" = "true" ]; then
    echo "Purging stopped containers (temporal echoes)..."
    docker container prune ${FORCE_FLAG} || echo "No stopped containers to purge."
fi

if [ "$PRUNE_IMAGES" = "true" ]; then
    echo "Purging dangling images (unanchored temporal snapshots)..."
    docker image prune ${FORCE_FLAG} || echo "No dangling images to purge."
    if [ "$PRUNE_ALL_IMAGES" = "true" ]; then
        echo "Purging all unused images (ancient temporal archives)..."
        docker image prune -a ${FORCE_FLAG} || echo "No unused images to purge."
    fi
fi

if [ "$PRUNE_VOLUMES" = "true" ]; then
    echo "Purging unused volumes (forgotten data dimensions)..."
    docker volume prune ${FORCE_FLAG} || echo "No unused volumes to purge."
fi

if [ "$PRUNE_NETWORKS" = "true" ]; then
    echo "Purging unused networks (collapsed spacetime conduits)..."
    docker network prune ${FORCE_FLAG} || echo "No unused networks to purge."
fi

echo ""
echo "Chrono-Purge Protocol Complete! Temporal integrity restored. Enjoy your tidier timeline."
