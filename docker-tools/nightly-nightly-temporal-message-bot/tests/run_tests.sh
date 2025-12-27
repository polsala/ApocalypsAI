#!/bin/bash

set -e

echo "Building Docker image for temporal-bottle..."
docker-compose -f docker-compose.yml build temporal-bottle

echo "Running tests inside the container..."
# Use 'docker-compose run --rm' to create a temporary container, run tests, and remove it.
# We specify the service name 'temporal-bottle' and the command to run tests.
# The working directory in the container is /app, so tests/test_app.py needs to be accessible.
# We mount the current directory (which contains src/ and tests/) into /app in the container.
docker run --rm \
  -v "$(pwd)/src":/app/src \
  -v "$(pwd)/tests":/app/tests \
  -w /app \
  $(docker images -q temporal-bottle_temporal-bottle | head -n 1) \
  python -m unittest tests/test_app.py

echo "Tests finished."
