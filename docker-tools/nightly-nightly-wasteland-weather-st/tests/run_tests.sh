#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

IMAGE_NAME="wasteland-weather-station-test"

echo "--- Building Docker image for testing ---"
docker build -t "$IMAGE_NAME" .

echo "--- Running unit tests inside the container ---"
# Run the container, and execute the Python unit tests.
# We use a temporary container (--rm) and override the CMD to run the tests.
# We also set dummy API_KEY and LOCATION as they are required by app.py's main execution path,
# but the tests mock the actual API call.
docker run --rm \
    -e API_KEY="DUMMY_API_KEY" \
    -e LOCATION="TestCity" \
    "$IMAGE_NAME" \
    python -m unittest tests/test_app.py

echo "--- All tests passed! ---"

# Optional: Basic functional test of the container (without mocking)
# This part is commented out to ensure tests are deterministic and offline by default.
# To run this, uncomment and set the OPENWEATHERMAP_API_KEY environment variable.
# echo "--- Running a basic functional test of the container (requires real API_KEY) ---"
# if [ -z "$OPENWEATHERMAP_API_KEY" ]; then
#     echo "Skipping functional test: OPENWEATHERMAP_API_KEY environment variable not set."
# else
#     echo "Running container with real API key for London..."
#     docker run --rm -e API_KEY="$OPENWEATHERMAP_API_KEY" -e LOCATION="London" "$IMAGE_NAME"
#     echo "Functional test complete (output above)."
# fi
