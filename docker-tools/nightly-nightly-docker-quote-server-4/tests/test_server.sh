#!/usr/bin/env bash
set -e

# Build the Docker image
docker build -t nightly-docker-quote-server-test -f Dockerfile .

# Run container in background, mapping host port 8081 to container port 8080
CONTAINER_ID=$(docker run -d -p 8081:8080 nightly-docker-quote-server-test)

# Give the server a moment to start
sleep 2

# Perform a request to the server
RESPONSE=$(curl -s http://localhost:8081)

# Expected quotes (must match the list in src/quote_server.py)
EXPECTED=(
    "The sun rose, but the world stayed dark."
    "Even the shadows have a deadline."
    "Hope is a candle in a storm of ash."
    "When the wind whispers, listen for the last song."
    "Survival is a game of dice and dust."
)

FOUND=0
for q in "${EXPECTED[@]}"; do
  if [[ "$RESPONSE" == "$q" ]]; then
    FOUND=1
    break
  fi
done

if [ $FOUND -ne 1 ]; then
  echo "Test failed: unexpected response: $RESPONSE"
  docker logs $CONTAINER_ID
  docker rm -f $CONTAINER_ID
  exit 1
fi

echo "Test passed: received expected quote."

# Clean up the container
docker rm -f $CONTAINER_ID
