#!/bin/bash

echo "🧹 Starting the Nightly Docker Dust Bunny Sweeper..."

# Clean up exited containers
echo "Searching for exited containers (digital dust bunnies)..."
EXPIRED_CONTAINERS=$(docker ps -a -f "status=exited" -q)
if [ -n "$EXPIRED_CONTAINERS" ]; then
    echo "Found these exited containers:"
    echo "$EXPIRED_CONTAINERS"
    docker rm $EXPIRED_CONTAINERS
    echo "Exited containers swept away!"
else
    echo "No exited containers (dust bunnies) found. Your digital space is tidy!"
fi

# Clean up dangling images
echo "Searching for dangling images (forgotten digital lint)..."
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$DANGLING_IMAGES" ]; then
    echo "Found these dangling images:"
    echo "$DANGLING_IMAGES"
    docker rmi $DANGLING_IMAGES
    echo "Dangling images swept away!"
else
    echo "No dangling images (lint) found. Your image registry is sparkling!"
fi

# Clean up dangling volumes
echo "Searching for dangling volumes (hidden digital fluff)..."
DANGLING_VOLUMES=$(docker volume ls -f "dangling=true" -q)
if [ -n "$DANGLING_VOLUMES" ]; then
    echo "Found these dangling volumes:"
    echo "$DANGLING_VOLUMES"
    docker volume rm $DANGLING_VOLUMES
    echo "Dangling volumes swept away!"
else
    echo "No dangling volumes (fluff) found. Your volume storage is pristine!"
fi

echo "✨ Nightly Docker Dust Bunny Sweeper finished its rounds. Your Docker environment is cleaner!"
