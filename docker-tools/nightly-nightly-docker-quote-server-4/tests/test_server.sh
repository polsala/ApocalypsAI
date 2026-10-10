#!/usr/bin/env bash
set -euo pipefail

# Build image
docker build -t nightly-docker-quote-server:test .

# Run container in background, map host 8081 -> container 8080
CONTAINER_ID=$(docker run -d -p 8081:8080 nightly-docker-quote-server:test)

# Give the server a moment to start
sleep 2

# Fetch deterministic quote (index=0)
RESPONSE=$(curl -s http://localhost:8081/quote?index=0)
EXPECTED='{"quote":"When the sky falls, remember to bring an umbrella."}'

if [[ "$RESPONSE" != "$EXPECTED" ]]; then
  echo "Test failed: expected $EXPECTED but got $RESPONSE"
  docker stop "$CONTAINER_ID" >/dev/null
  docker rm "$CONTAINER_ID" >/dev/null
  exit 1
fi

# Clean up container
docker stop "$CONTAINER_ID" >/dev/null
docker rm "$CONTAINER_ID" >/dev/null

echo "All tests passed."
