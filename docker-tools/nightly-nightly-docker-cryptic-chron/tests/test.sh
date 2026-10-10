#!/usr/bin/env bash
set -e

# Build the Docker image
docker build -t cryptic-chronicle-test . > /dev/null

# Run container in background with deterministic seed
container_id=$(docker run -d -p 8081:8080 -e FORTUNE_SEED=5 cryptic-chronicle-test)

# Give server time to start
sleep 1

# Fetch prophecy
output=$(curl -s http://localhost:8081)

# Expected JSON (seed 5 -> index 1)
expected='{"prophecy":"Rats will inherit the throne."}'

if [ "$output" != "$expected" ]; then
    echo "Test failed: expected $expected but got $output"
    docker rm -f "$container_id"
    exit 1
fi

# Cleanup
docker rm -f "$container_id"
docker rmi -f cryptic-chronicle-test > /dev/null

echo "All tests passed."
