#!/bin/bash

set -euo pipefail

IMAGE_NAME="temporal-replay-box-test"
CONTAINER_NAME="temporal-replay-box-test-instance"
PORT="8080"

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" .

echo "--- Running Docker container ---"
docker run -d --name "$CONTAINER_NAME" -p "$PORT":"$PORT" "$IMAGE_NAME"

# Mock rationale: Using sleep to ensure the server has time to start up before sending requests.
# This makes the test deterministic and reliable in a local containerized environment.
sleep 3

echo "--- Sending test POST request to /echo/data ---"
curl_output=$(curl -s -X POST -H "Content-Type: application/json" -d '{"test_key": "test_value"}' "http://localhost:$PORT/echo/data")

if [[ "$curl_output" != *"Request recorded successfully!"* ]]; then
    echo "Test POST request failed: Unexpected response: $curl_output"
    docker logs "$CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    docker rmi "$IMAGE_NAME" > /dev/null
    exit 1
fi

echo "--- Sending test GET request to /echo/status ---"
curl_output=$(curl -s "http://localhost:$PORT/echo/status")

if [[ "$curl_output" != *"Request recorded successfully!"* ]]; then
    echo "Test GET request failed: Unexpected response: $curl_output"
    docker logs "$CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    docker rmi "$IMAGE_NAME" > /dev/null
    exit 1
fi

echo "--- Fetching history from /history ---"
history_json=$(curl -s "http://localhost:$PORT/history")

# Mock rationale: Using grep to check for expected content in the JSON response.
# This is an offline check against the locally generated output.
if ! echo "$history_json" | grep -q '"method": "POST"' || \
   ! echo "$history_json" | grep -q '"url": "/echo/data"' || \
   ! echo "$history_json" | grep -q '"body": "{\"test_key\": \"test_value\"}"' || \
   ! echo "$history_json" | grep -q '"method": "GET"' || \
   ! echo "$history_json" | grep -q '"url": "/echo/status"'; then
    echo "History verification failed: Expected recorded requests not found."
    echo "Full history:"
    echo "$history_json"
    docker logs "$CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    docker rmi "$IMAGE_NAME" > /dev/null
    exit 1
fi

echo "--- All tests passed successfully! ---"

echo "--- Cleaning up Docker resources ---"
docker stop "$CONTAINER_NAME" > /dev/null
docker rm "$CONTAINER_NAME" > /dev/null
docker rmi "$IMAGE_NAME" > /dev/null
