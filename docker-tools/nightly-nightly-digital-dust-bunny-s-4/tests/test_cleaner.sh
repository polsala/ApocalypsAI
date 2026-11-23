#!/bin/bash
set -euo pipefail

# Setup mock environment
TEST_DIR=$(mktemp -d)
MOCK_DOCKER_PATH="${TEST_DIR}/docker"
MOCK_LOG_FILE="${TEST_DIR}/docker_calls.log"
export MOCK_LOG_FILE # Make it available to the mock script

# Create mock docker executable
cat << 'EOF' > "$MOCK_DOCKER_PATH"
#!/bin/bash
# Mock rationale: This mock simulates the docker CLI behavior for pruning commands
# without actually interacting with a Docker daemon, ensuring deterministic and offline tests.
# It logs the commands it receives to a file, which the test script then asserts against.
echo "MOCK DOCKER CALLED: $@" >> "$MOCK_LOG_FILE"
# Simulate success for prune commands
if [[ "$@" =~ "prune" ]]; then
    echo "Total reclaimed space: 0B" # Simulate output
    exit 0
fi
# Simulate docker socket existence check (e.g., for 'docker info' which might be implicitly called by some docker clients)
if [[ "$@" == "info" ]]; then
    echo "Containers: 0" # Minimal output to simulate success
    exit 0
fi
exit 0
EOF
chmod +x "$MOCK_DOCKER_PATH"

# Temporarily add mock docker to PATH
export PATH="${TEST_DIR}:${PATH}"

# Mock rationale: Create a dummy docker.sock file to satisfy the existence check in cleaner.sh
# This ensures the script proceeds to call the mocked 'docker' command, making the test deterministic.
mkdir -p /var/run # Ensure directory exists for the mock socket
touch /var/run/docker.sock

# Test cases

# Test 1: Default (all, 24h)
echo "Running test: default (all, 24h)"
./src/cleaner.sh > /dev/null 2>&1
grep -q "MOCK DOCKER CALLED: system prune --force --filter until=24h" "$MOCK_LOG_FILE" || { echo "Test failed: default prune command not called."; exit 1; }
echo "Test passed: default (all, 24h)"
rm "$MOCK_LOG_FILE" && touch "$MOCK_LOG_FILE" # Clear log for next test

# Test 2: images, 7d
echo "Running test: images, 7d"
./src/cleaner.sh images 7d > /dev/null 2>&1
grep -q "MOCK DOCKER CALLED: image prune --force --filter until=7d" "$MOCK_LOG_FILE" || { echo "Test failed: images prune command not called."; exit 1; }
echo "Test passed: images, 7d"
rm "$MOCK_LOG_FILE" && touch "$MOCK_LOG_FILE" # Clear log for next test

# Test 3: volumes, 1h
echo "Running test: volumes, 1h"
./src/cleaner.sh volumes 1h > /dev/null 2>&1
grep -q "MOCK DOCKER CALLED: volume prune --force --filter until=1h" "$MOCK_LOG_FILE" || { echo "Test failed: volumes prune command not called."; exit 1; }
echo "Test passed: volumes, 1h"
rm "$MOCK_LOG_FILE" && touch "$MOCK_LOG_FILE" # Clear log for next test

# Test 4: networks, 30m
echo "Running test: networks, 30m"
./src/cleaner.sh networks 30m > /dev/null 2>&1
grep -q "MOCK DOCKER CALLED: network prune --force --filter until=30m" "$MOCK_LOG_FILE" || { echo "Test failed: networks prune command not called."; exit 1; }
echo "Test passed: networks, 30m"
rm "$MOCK_LOG_FILE" && touch "$MOCK_LOG_FILE" # Clear log for next test

# Test 5: Invalid mode
echo "Running test: invalid mode"
if ./src/cleaner.sh invalid_mode 1h > /dev/null 2>&1; then
    echo "Test failed: invalid mode should exit with error."; exit 1;
else
    echo "Test passed: invalid mode correctly exited with error."
fi

echo "All tests passed!"

# Cleanup
rm -rf "$TEST_DIR"
# Mock rationale: Remove the dummy docker.sock file created for testing to prevent side effects
# and ensure a clean state for subsequent test runs.
rm /var/run/docker.sock
