#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output)
docker build -t quote-server-test . > /dev/null

# Run container in background with a known QUOTE_INDEX
container_id=$(docker run -d -e QUOTE_INDEX=2 -p 8080:8080 quote-server-test)
# Give the server a moment to start
sleep 2
# Query the endpoint
output=$(curl -s http://localhost:8080/quote)
# Clean up the container
docker rm -f "$container_id" > /dev/null

# Expected JSON fragment (mock rationale: deterministic quote at index 2)
expected='"quote":"Keep your water filter close and your jokes closer."'

if echo "$output" | grep -q "$expected"; then
    echo "PASS"
    exit 0
else
    echo "FAIL: unexpected output -> $output"
    exit 1
fi
