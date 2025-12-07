#!/bin/sh

# Digital gardening metaphors for Docker cleanup
GHOST_CONTAINERS=$(docker ps -a -f status=exited --format "{{.ID}}")
GHOST_IMAGES=$(docker images -f "dangling=true" -q)
GHOST_VOLUMES=$(docker volume ls -f "dangling=true" -q)

if [ "$1" = "--whisper" ]; then
  echo "🌱 Scanning for digital weeds..."
fi

if [ -n "$GHOST_CONTAINERS" ]; then
  if [ "$1" = "--whisper" ]; then
    echo "🪓 Uprooting ghost containers..."
  fi
  docker rm $GHOST_CONTAINERS > /dev/null
fi

if [ -n "$GHOST_IMAGES" ]; then
  if [ "$1" = "--whisper" ]; then
    echo "🧹 Clearing abandoned images..."
  fi
  docker rmi $GHOST_IMAGES > /dev/null
fi

if [ -n "$GHOST_VOLUMES" ]; then
  if [ "$1" = "--whisper" ]; then
    echo "🗑️  Removing rootless volumes..."
  fi
  docker volume rm $GHOST_VOLUMES > /dev/null
fi

if [ "$1" = "--whisper" ]; then
  echo "✨ Your Docker garden is now pruned and flourishing!"
fi
