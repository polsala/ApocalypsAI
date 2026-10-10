#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

IMAGE_NAME="nightly-beacon-generator"
CONTAINER_NAME="beacon-service-test"
HOST_PORT="8081" # Use a different port for tests to avoid conflicts
CONTAINER_PORT="5000"
API_ENDPOINT="http://localhost:$HOST_PORT/generate_beacon"

# --- Helper functions ---
log_info() {
    echo "INFO: $1"
}

log_error() {
    echo "ERROR: $1" >&2
    exit 1
}

cleanup() {
    log_info "Cleaning up..."
    docker stop "$CONTAINER_NAME" > /dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
    log_info "Cleanup complete."
}

# Register cleanup function to run on exit
trap cleanup EXIT

# --- Test steps ---

log_info "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" . || log_error "Failed to build Docker image."

log_info "Stopping and removing any existing test container: $CONTAINER_NAME"
docker stop "$CONTAINER_NAME" > /dev/null 2>&1 || true
docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true

log_info "Running Docker container for tests: $CONTAINER_NAME on port $HOST_PORT"
docker run -d -p "$HOST_PORT":"$CONTAINER_PORT" --name "$CONTAINER_NAME" "$IMAGE_NAME" || log_error "Failed to run Docker container."

log_info "Waiting for service to become available..."
MAX_RETRIES=10
RETRY_COUNT=0
until curl -s "$API_ENDPOINT" > /dev/null; do
    if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
        log_error "Service did not become available after $MAX_RETRIES retries."
    fi
    log_info "Service not yet available, retrying in 2 seconds..."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT+1))
done
log_info "Service is available."

# --- Test Case 1: Basic beacon generation ---
log_info "Test Case 1: Basic beacon generation (no parameters)"
RESPONSE=$(curl -s "$API_ENDPOINT")
log_info "Response: $RESPONSE"

# Mock rationale: We are testing the containerized service's API response structure and content,
# not external dependencies. The 'curl' command interacts directly with the local container.
# The 'jq' command is used to parse the JSON response, which is a standard tool for this.
# The randomness of the description is controlled by seeding within the app, making it deterministic for a given ID.
# The ID's exact value is not asserted, only its format and presence.

if ! echo "$RESPONSE" | jq -e '.id | type == "string" and length == 64' > /dev/null; then
    log_error "Test Case 1 Failed: 'id' field is missing or not a 64-char string."
fi
if ! echo "$RESPONSE" | jq -e '.description | type == "string" and length > 0' > /dev/null; then
    log_error "Test Case 1 Failed: 'description' field is missing or empty."
}
if ! echo "$RESPONSE" | jq -e '.timestamp | type == "string"' > /dev/null; then
    log_error "Test Case 1 Failed: 'timestamp' field is missing or not a string."
fi
log_info "Test Case 1 Passed."

# --- Test Case 2: Beacon generation with location parameter ---
log_info "Test Case 2: Beacon generation with 'location' parameter"
LOCATION="Old Water Tower"
ENCODED_LOCATION=$(echo "$LOCATION" | jq -sRr @uri) # URL-encode
RESPONSE_LOCATION=$(curl -s "$API_ENDPOINT?location=$ENCODED_LOCATION")
log_info "Response with location: $RESPONSE_LOCATION"

if ! echo "$RESPONSE_LOCATION" | jq -e '.id | type == "string" and length == 64' > /dev/null; then
    log_error "Test Case 2 Failed: 'id' field is missing or not a 64-char string."
fi
if ! echo "$RESPONSE_LOCATION" | jq -e '.description | type == "string" and length > 0' > /dev/null; then
    log_error "Test Case 2 Failed: 'description' field is missing or empty."
fi
log_info "Test Case 2 Passed."

# --- Test Case 3: Beacon generation with location and purpose parameters ---
log_info "Test Case 3: Beacon generation with 'location' and 'purpose' parameters"
LOCATION="Abandoned Mine"
PURPOSE="Resource Cache"
ENCODED_LOCATION=$(echo "$LOCATION" | jq -sRr @uri)
ENCODED_PURPOSE=$(echo "$PURPOSE" | jq -sRr @uri)
RESPONSE_FULL=$(curl -s "$API_ENDPOINT?location=$ENCODED_LOCATION&purpose=$ENCODED_PURPOSE")
log_info "Response with location and purpose: $RESPONSE_FULL"

if ! echo "$RESPONSE_FULL" | jq -e '.id | type == "string" and length == 64' > /dev/null; then
    log_error "Test Case 3 Failed: 'id' field is missing or not a 64-char string."
fi
if ! echo "$RESPONSE_FULL" | jq -e '.description | type == "string" and length > 0' > /dev/null; then
    log_error "Test Case 3 Failed: 'description' field is missing or empty."
fi
log_info "Test Case 3 Passed."

log_info "All tests passed successfully!"
