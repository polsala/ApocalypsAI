#!/bin/bash

# Mocking functions for docker-compose
_mock_docker_compose() {
    echo "Mocking docker-compose: $@"
    # Simulate success for 'up -d' and 'down'
    if [[ "$@" == "up -d" || "$@" == "down" ]]; then
        return 0
    else
        return 1
    fi
}

# Replace actual docker-compose with our mock
_original_docker_compose() { docker-compose "$@"; }

# Function to run tests
run_test() {
    local test_name="$1"
    local expected_output="$2"
    local command_to_run="$3"
    local actual_output=$(eval "$command_to_run" 2>&1)

    echo "Running test: $test_name"
    if echo "$actual_output" | grep -q "$expected_output"; then
        echo "  PASSED"
    else
        echo "  FAILED"
        echo "    Expected: $expected_output"
        echo "    Got: $actual_output"
        return 1
    fi
    return 0
}

# --- Test Setup ---

# Create a dummy docker-compose.yml for testing
cat <<EOF > docker-compose.yml
version: '3.8'
services:
  test_service:
    image: alpine:latest
EOF

# Mock docker-compose command
_mock_docker_compose_cmd() {
    _mock_docker_compose "$@"
}

# Alias docker-compose to our mock function
docker-compose() {
    _mock_docker_compose_cmd "$@"
}

# --- Test Cases ---

# Test case 1: Starting the environment
if ! run_test "Start Environment" "Docker environment started successfully." "./src/docker-env-manager start"; then
    exit 1
fi

# Test case 2: Stopping the environment
if ! run_test "Stop Environment" "Docker environment stopped successfully." "./src/docker-env-manager stop"; then
    exit 1
fi

# Test case 3: Missing docker-compose.yml
# Temporarily remove the dummy file
rm docker-compose.yml
if ! run_test "Missing Compose File" "Error: docker-compose.yml not found" "./src/docker-env-manager start"; then
    exit 1
fi

# Restore the dummy file for potential future tests or cleanup
cat <<EOF > docker-compose.yml
version: '3.8'
services:
  test_service:
    image: alpine:latest
EOF

# --- Cleanup ---
rm docker-compose.yml

echo "All tests completed."
exit 0
