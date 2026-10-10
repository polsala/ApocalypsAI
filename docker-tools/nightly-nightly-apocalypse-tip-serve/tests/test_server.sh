#!/usr/bin/env bash
set -e

# Build the Docker image
docker build -t tip-test . > /dev/null

# Run the container with a known seed (7) and map to host port 18080
container_id=$(docker run -d -e SEED=7 -p 18080:8080 tip-test)

# Ensure the container is cleaned up on exit
cleanup() {
    docker rm -f "$container_id" > /dev/null 2>&1 || true
    docker rmi tip-test > /dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait a moment for the server to start
sleep 1

# Query the server
response=$(curl -s http://localhost:18080/)

# Expected tip: index = 7 % 5 = 2 -> "Water is more valuable than gold."
expected="Water is more valuable than gold."

if [ "$response" != "$expected" ]; then
    echo "FAIL: expected '$expected' but got '$response'"
    exit 1
fi

echo "PASS"
