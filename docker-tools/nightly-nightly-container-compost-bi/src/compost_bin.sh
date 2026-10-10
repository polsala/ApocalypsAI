#!/bin/bash

# Default values
COMPOST_DAYS_OLD=${COMPOST_DAYS_OLD:-7}

# Convert days to hours for Docker filters
COMPOST_HOURS_OLD=$((COMPOST_DAYS_OLD * 24))

echo "ApocalypsAI Container Compost Bin initiated!"
echo "Pruning resources older than ${COMPOST_DAYS_OLD} days (${COMPOST_HOURS_OLD} hours)."
echo "---"

# Prune stopped containers
echo "Composting stopped containers..."
# Prune containers that have been stopped for more than COMPOST_HOURS_OLD
docker container prune --force --filter "until=${COMPOST_HOURS_OLD}h"
if [ $? -ne 0 ]; then
    echo "Warning: Container pruning failed or encountered issues."
fi
echo "---"

# Prune dangling images
echo "Composting dangling images (untagged and not referenced by any container)..."
docker image prune --force --filter "dangling=true"
if [ $? -ne 0 ]; then
    echo "Warning: Dangling image pruning failed or encountered issues."
}
echo "---"

# Prune unused images (not associated with any container) older than COMPOST_HOURS_OLD
echo "Composting other unused images (not associated with any container) older than ${COMPOST_HOURS_OLD} hours..."
# Note: `docker image prune --filter "until=Xh"` prunes images that are not associated with any container
# AND were created before X hours ago. This is a good general prune.
docker image prune --force --filter "until=${COMPOST_HOURS_OLD}h"
if [ $? -ne 0 ]; then
    echo "Warning: Unused image pruning failed or encountered issues."
}
echo "---"

# Prune unused volumes
echo "Composting unused volumes (not associated with any container) older than ${COMPOST_HOURS_OLD} hours..."
docker volume prune --force --filter "until=${COMPOST_HOURS_OLD}h"
if [ $? -ne 0 ]; then
    echo "Warning: Volume pruning failed or encountered issues."
}
echo "---"

echo "ApocalypsAI Container Compost Bin finished its work. Your digital garden is tidier!"
