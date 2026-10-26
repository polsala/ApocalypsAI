#!/usr/bin/env bash
set -e

# Build the Docker image
docker build -t nightly-survival-tip-test . > /dev/null

# Run container in background, expose on host port 8081
CONTAINER_ID=$(docker run -d -p 8081:8080 -e TIP_INDEX=2 nightly-survival-tip-test)

# Give server time to start
sleep 2

# Query the server
RESPONSE=$(curl -s http://localhost:8081)

# Expected tip (index 2)
EXPECTED="Map your routes; the wasteland changes daily."

# Check response contains expected tip
if echo "$RESPONSE" | grep -q "$EXPECTED"; then
    echo "Test passed"
    docker rm -f "$CONTAINER_ID" > /dev/null
    exit 0
else
    echo "Test failed: expected tip not found"
    docker logs "$CONTAINER_ID"
    docker rm -f "$CONTAINER_ID" > /dev/null
    exit 1
fi
