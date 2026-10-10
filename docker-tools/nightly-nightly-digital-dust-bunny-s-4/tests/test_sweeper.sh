#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

# Setup a temporary directory for mocks and logs
TEST_DIR=$(mktemp -d)
MOCK_BIN="$TEST_DIR/bin"
LOG_FILE="$TEST_DIR/mock_docker.log"
mkdir -p "$MOCK_BIN"

# Mock rationale: The 'docker' command is mocked to ensure tests are deterministic and offline.
# Instead of actually interacting with a Docker daemon, this mock captures the commands that
# dust_bunny_sweeper.sh *would* execute, allowing verification of the script's logic without
# requiring a live Docker environment or risking actual system changes.
cat << 'EOF' > "$MOCK_BIN/docker"
#!/bin/bash
echo "MOCK_DOCKER_CALL: $@" >> "$LOG_FILE"
# Simulate success for prune commands
if [[ "$1" == "image" && "$2" == "prune" ]]; then
    echo "Total reclaimed space: 100MB"
elif [[ "$1" == "volume" && "$2" == "prune" ]]; then
    echo "Total reclaimed space: 50MB"
elif [[ "$1" == "network" && "$2" == "prune" ]]; then
    echo "Total reclaimed space: 10MB"
elif [[ "$1" == "builder" && "$2" == "prune" ]]; then
    echo "Total reclaimed space: 200MB"
fi
EOF
chmod +x "$MOCK_BIN/docker"

# Store original PATH and set a new one for testing
OLD_PATH="$PATH"
export PATH="$MOCK_BIN:$PATH"

# Source the script to be tested (or run it directly)
SWEAPER_SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# --- Test Case 1: Default Dry Run ---
echo "--- Running Test Case 1: Default Dry Run ---"
# Clear log file for this test
> "$LOG_FILE"
OUTPUT=$(DRY_RUN=true bash "$SWEAPER_SCRIPT_PATH")

# Assertions for Dry Run output
if echo "$OUTPUT" | grep -q "Dry Run mode active!"; then
    echo "PASS: Dry Run mode detected in output."
else
    echo "FAIL: Dry Run mode NOT detected in output."
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "Would run: docker image prune --filter \"until=24h\""; then
    echo "PASS: Image prune dry run command logged."
else
    echo "FAIL: Image prune dry run command NOT logged."
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "Would run: docker volume prune --filter \"until=24h\""; then
    echo "PASS: Volume prune dry run command logged."
else
    echo "FAIL: Volume prune dry run command NOT logged."
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "Would run: docker network prune --filter \"until=24h\""; then
    echo "PASS: Network prune dry run command logged."
else
    echo "FAIL: Network prune dry run command NOT logged."
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "Would run: docker builder prune --all --filter \"until=24h\""; then
    echo "PASS: Builder prune dry run command logged."
else
    echo "FAIL: Builder prune dry run command NOT logged."
    echo "$OUTPUT"
    exit 1
fi

# Assertions for mock docker calls (should be none in dry run, as it only logs "Would run")
if grep -q "MOCK_DOCKER_CALL" "$LOG_FILE"; then
    echo "FAIL: Mock docker was called during dry run. Log content:"
    cat "$LOG_FILE"
    exit 1
else
    echo "PASS: Mock docker was NOT called during dry run, as expected."
fi

# --- Test Case 2: Actual Cleanup Run ---
echo "--- Running Test Case 2: Actual Cleanup Run ---"
# Clear log file for this test
> "$LOG_FILE"
OUTPUT=$(DRY_RUN=false bash "$SWEAPER_SCRIPT_PATH")

# Assertions for Actual Run output
if echo "$OUTPUT" | grep -q "Initiating deep clean!"; then
    echo "PASS: Actual cleanup mode detected in output."
else
    echo "FAIL: Actual cleanup mode NOT detected in output."
    echo "$OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "Cleanup complete!"; then
    echo "PASS: Cleanup completion message detected."
else
    echo "FAIL: Cleanup completion message NOT detected."
    echo "$OUTPUT"
    exit 1
fi

# Assertions for mock docker calls (should be present)
if grep -q "MOCK_DOCKER_CALL: image prune --force --filter until=24h" "$LOG_FILE" && \
   grep -q "MOCK_DOCKER_CALL: image prune --force --filter dangling=true" "$LOG_FILE" && \
   grep -q "MOCK_DOCKER_CALL: volume prune --force --filter until=24h" "$LOG_FILE" && \
   grep -q "MOCK_DOCKER_CALL: network prune --force --filter until=24h" "$LOG_FILE" && \
   grep -q "MOCK_DOCKER_CALL: builder prune --force --all --filter until=24h" "$LOG_FILE"; then
    echo "PASS: All expected mock docker prune commands were called."
else
    echo "FAIL: Not all expected mock docker prune commands were called. Log content:"
    cat "$LOG_FILE"
    exit 1
fi

# --- Test Case 3: Custom Configuration (e.g., only images, 7 days old) ---
echo "--- Running Test Case 3: Custom Configuration (Images only, 7 days) ---"
# Clear log file for this test
> "$LOG_FILE"
OUTPUT=$(DRY_RUN=false MAX_AGE_HOURS=168 CLEANUP_VOLUMES=false CLEANUP_NETWORKS=false CLEANUP_BUILD_CACHE=false bash "$SWEAPER_SCRIPT_PATH")

# Assertions for output
if echo "$OUTPUT" | grep -q "Skipping volume cleanup"; then
    echo "PASS: Skipping volume cleanup message detected."
else
    echo "FAIL: Skipping volume cleanup message NOT detected."
    echo "$OUTPUT"
    exit 1
fi
if echo "$OUTPUT" | grep -q "Skipping network cleanup"; then
    echo "PASS: Skipping network cleanup message detected."
else
    echo "FAIL: Skipping network cleanup message NOT detected."
    echo "$OUTPUT"
    exit 1
fi
if echo "$OUTPUT" | grep -q "Skipping build cache cleanup"; then
    echo "PASS: Skipping build cache cleanup message detected."
else
    echo "FAIL: Skipping build cache cleanup message NOT detected."
    echo "$OUTPUT"
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "Skipping image cleanup"; then
    echo "PASS: Image cleanup not skipped."
else
    echo "FAIL: Image cleanup was unexpectedly skipped."
    echo "$OUTPUT"
    exit 1
fi

# Assertions for mock docker calls
if grep -q "MOCK_DOCKER_CALL: image prune --force --filter until=168h" "$LOG_FILE" && \
   grep -q "MOCK_DOCKER_CALL: image prune --force --filter dangling=true" "$LOG_FILE" && \
   ! grep -q "MOCK_DOCKER_CALL: volume prune" "$LOG_FILE" && \
   ! grep -q "MOCK_DOCKER_CALL: network prune" "$LOG_FILE" && \
   ! grep -q "MOCK_DOCKER_CALL: builder prune" "$LOG_FILE"; then
    echo "PASS: Only expected image prune commands were called with correct age."
else
    echo "FAIL: Incorrect mock docker calls for custom config. Log content:"
    cat "$LOG_FILE"
    exit 1
fi

# Cleanup
export PATH="$OLD_PATH"
rm -rf "$TEST_DIR"

echo "All tests passed successfully!"
exit 0
