#!/bin/bash
# Cleanup script for Nightly Docker Chaos Monkey

set -e

echo "🧹 Cleaning up Nightly Docker Chaos Monkey..."

# Stop and remove chaos monkey containers
echo "Stopping chaos monkey containers..."
docker stop chaos-monkey 2>/dev/null || true
docker rm chaos-monkey 2>/dev/null || true
docker stop chaos-monkey-test 2>/dev/null || true
docker rm chaos-monkey-test 2>/dev/null || true

docker stop chaos-monkey-dry-run 2>/dev/null || true
docker rm chaos-monkey-dry-run 2>/dev/null || true

docker stop chaos-dashboard 2>/dev/null || true
docker rm chaos-dashboard 2>/dev/null || true

# Remove test containers
echo "Removing test containers..."
docker stop test-app test-app-2 test-target 2>/dev/null || true
docker rm test-app test-app-2 test-target 2>/dev/null || true

# Remove chaos monkey image
echo "Removing chaos monkey image..."
docker rmi nightly-docker-chaos-monkey:latest 2>/dev/null || true

# Clean up any containers with chaos.monkey label
echo "Cleaning up containers with chaos.monkey label..."
for container in $(docker ps -q --filter "label=chaos.monkey=true"); do
    echo "Stopping container: $container"
    docker stop "$container" 2>/dev/null || true
    docker rm "$container" 2>/dev/null || true
done

# Clean up any dangling images and volumes
echo "Cleaning up dangling images and volumes..."
docker image prune -f
docker volume prune -f

echo "✅ Cleanup complete!"
echo ""
echo "Note: You may need to manually remove any containers that were not stopped properly."
