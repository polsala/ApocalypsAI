#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: All external interactions are confined to Docker which runs locally; no network calls.

# Build the Docker image
docker build -t quote-espresso-test ./docker-tools/nightly-docker-quote-espresso > /dev/null

# Run the container in the background
container_id=$(docker run -d -p 8081:8080 quote-espresso-test)

# Ensure container is cleaned up on exit
cleanup() {
    docker rm -f "$container_id" > /dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for the server to become reachable (max 5 seconds)
for i in {1..5}; do
    if curl -s http://localhost:8081/quote > /dev/null; then
        break
    fi
    sleep 1
done

# Fetch a quote
response=$(curl -s http://localhost:8081/quote)

# Expected quotes (must match the list in main.go)
expected=(
    "Coffee is the gasoline of the soul."
    "Life begins after coffee."
    "Espresso yourself!"
    "May your coffee be strong and your code be bug‑free."
    "When in doubt, add more coffee."
)

# Extract the quote field using jq (install jq in the test environment or use simple parsing)
quote=$(echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['quote'])")

# Verify the quote is one of the expected ones
found=false
for exp in "${expected[@]}"; do
    if [[ "$quote" == "$exp" ]]; then
        found=true
        break
    fi
done

if [[ "$found" == true ]]; then
    echo "Test passed: received expected quote -> $quote"
    exit 0
else
    echo "Test failed: unexpected quote -> $quote"
    exit 1
fi
