#!/bin/bash

# Whimsical Docker Dust Bunny Sweeper

echo "✨ Initiating the Nightly Docker Dust Bunny Sweeper... ✨"
echo "Scanning your container garden for forgotten bits and bobs!"
echo "---------------------------------------------------------"

# Find dangling images
echo "🔍 Checking for forgotten image remnants (dangling images)..."
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
NUM_DANGLING_IMAGES=$(echo "$DANGLING_IMAGES" | grep -c .)
if [ "$NUM_DANGLING_IMAGES" -gt 0 ]; then
    echo "  Found $NUM_DANGLING_IMAGES digital dust bunnies in your image collection!"
    echo "$DANGLING_IMAGES" | sed 's/^/    - /' # Indent list
else
    echo "  Your image registry is sparkling clean! No dangling images found."
fi
echo ""

# Find unused volumes
echo "🔍 Peeking under the rug for orphaned data piles (unused volumes)..."
UNUSED_VOLUMES=$(docker volume ls -f "dangling=true" -q)
NUM_UNUSED_VOLUMES=$(echo "$UNUSED_VOLUMES" | grep -c .)
if [ "$NUM_UNUSED_VOLUMES" -gt 0 ]; then
    echo "  Discovered $NUM_UNUSED_VOLUMES forgotten data clumps!"
    echo "$UNUSED_VOLUMES" | sed 's/^/    - /'
else
    echo "  All your data volumes are neatly organized! No unused volumes found."
fi
echo ""

# Find unused networks
echo "🔍 Untangling forgotten network threads (unused networks)..."
# Using --dry-run to list networks that would be pruned without actually deleting them.
UNUSED_NETWORKS_REPORT=$(docker network prune --force --dry-run 2>&1)
# Extract network IDs and names from the dry-run output.
# Example output: "Would delete network <id> (<name>)"
UNUSED_NETWORKS=$(echo "$UNUSED_NETWORKS_REPORT" | grep "Would delete network" | sed -E 's/.*Would delete network ([a-f0-9]+) \(([^)]*)\).*/\1 (\2)/')
NUM_UNUSED_NETWORKS=$(echo "$UNUSED_NETWORKS" | grep -c .)

if [ "$NUM_UNUSED_NETWORKS" -gt 0 ]; then
    echo "  Found $NUM_UNUSED_NETWORKS tangled network threads!"
    echo "$UNUSED_NETWORKS" | sed 's/^/    - /'
else
    echo "  Your network pathways are clear! No unused networks found."
fi
echo ""

echo "---------------------------------------------------------"
echo "🧹 Sweeping complete! Your container environment is now more aware of its digital dust bunnies."
echo "Consider running 'docker system prune' or specific 'docker image prune', 'docker volume prune', 'docker network prune' to tidy up!"
echo "✨ Happy container gardening! ✨"
