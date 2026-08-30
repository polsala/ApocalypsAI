#!/bin/bash
set -e

# Default values
PRUNE_ALL_VOLUMES=${PRUNE_ALL_VOLUMES:-"false"}
PRUNE_ALL_IMAGES=${PRUNE_ALL_IMAGES:-"false"} # Prune all unused images, not just dangling
PRUNE_NETWORKS=${PRUNE_NETWORKS:-"false"}
PRUNE_BUILD_CACHE=${PRUNE_BUILD_CACHE:-"false"}

echo "Starting Nightly Container Composter..."
echo "Configuration:"
echo "  PRUNE_ALL_VOLUMES: ${PRUNE_ALL_VOLUMES}"
echo "  PRUNE_ALL_IMAGES: ${PRUNE_ALL_IMAGES}"
echo "  PRUNE_NETWORKS: ${PRUNE_NETWORKS}"
echo "  PRUNE_BUILD_CACHE: ${PRUNE_BUILD_CACHE}"

# Prune stopped containers
echo "Pruning stopped containers..."
docker container prune -f || true # Use || true to prevent script from exiting if no containers to prune

# Prune dangling images
echo "Pruning dangling images..."
docker image prune -f || true

# Prune all unused images (if configured)
if [ "${PRUNE_ALL_IMAGES}" = "true" ]; then
    echo "Pruning all unused images..."
    docker image prune -a -f || true
fi

# Prune unused volumes (if configured)
if [ "${PRUNE_ALL_VOLUMES}" = "true" ]; then
    echo "Pruning all unused volumes..."
    docker volume prune -f || true
fi

# Prune unused networks (if configured)
if [ "${PRUNE_NETWORKS}" = "true" ]; then
    echo "Pruning unused networks..."
    docker network prune -f || true
fi

# Prune build cache (if configured)
if [ "${PRUNE_BUILD_CACHE}" = "true" ]; then
    echo "Pruning build cache..."
    docker builder prune -f || true
fi

echo "Nightly Container Composter finished its work. Your pods are now tidier!"
