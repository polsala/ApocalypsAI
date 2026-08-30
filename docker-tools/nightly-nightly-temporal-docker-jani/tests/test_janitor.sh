#!/bin/bash
set -euo pipefail

# Create a temporary directory for our mock docker binary
MOCK_BIN_DIR=$(mktemp -d)
MOCK_DOCKER_BIN="$MOCK_BIN_DIR/docker"

# Mock rationale: We need to simulate docker command output without actually running docker.
# This mock script replaces the real 'docker' binary during tests, providing predefined responses.
cat << 'EOF' > "$MOCK_DOCKER_BIN"
#!/bin/bash
case "$1" in
    "ps")
        if [[ "$2" == "-a" && "$3" == "--filter" && "$4" == "status=exited" && "$5" == "-q" ]]; then
            # Mock rationale: Simulate two exited containers, one old, one recent.
            echo "container_id_old"
            echo "container_id_recent"
        else
            echo "Error: Unexpected docker ps command: $*" >&2
            exit 1
        fi
        ;;
    "inspect")
        if [[ "$2" == "container_id_old" ]]; then
            # Mock rationale: Simulate an old container finished long ago (before 2024-07-25 - 30 days).
            echo '{"State": {"FinishedAt": "2023-01-01T00:00:00.000000000Z"}}'
        elif [[ "$2" == "container_id_recent" ]]; then
            # Mock rationale: Simulate a recent container finished recently (after 2024-07-25 - 30 days).
            echo '{"State": {"FinishedAt": "2024-07-25T10:00:00.000000000Z"}}'
        else
            echo "Error: Unexpected docker inspect command: $*" >&2
            exit 1
        fi
        ;;
    "images")
        if [[ "$2" == "-f" && "$3" == "dangling=true" && "$4" == "-q" ]]; then
            # Mock rationale: Simulate one dangling image.
            echo "dangling_image_id"
        else
            echo "Error: Unexpected docker images command: $*" >&2
            exit 1
        fi
        ;;
    "rm")
        # Mock rationale: Simulate successful container removal.
        echo "Removed container $2"
        ;;
    "rmi")
        # Mock rationale: Simulate successful image removal.
        echo "Removed image $2"
        ;;
    *)
        echo "Error: Unexpected docker command: $*" >&2
        exit 1
        ;;
esac
EOF
chmod +x "$MOCK_DOCKER_BIN"

# Add the mock binary directory to the PATH for the test script
export PATH="$MOCK_BIN_DIR:$PATH"

# Mock rationale: Set a fixed current date for deterministic testing.
# This ensures that date comparisons in the script are consistent across test runs.
CURRENT_TEST_DATE="2024-07-25T12:00:00Z"
export TEST_CURRENT_DATE_OVERRIDE="$CURRENT_TEST_DATE"

# --- Test 1: Dry run, should list but not remove ---
echo "--- Test 1: Dry run (should list old container and dangling image) ---"
OUTPUT=$(./src/temporal_janitor.sh --dry-run --days-old 30)
if echo "$OUTPUT" | grep -q "container_id_old" && \
   echo "$OUTPUT" | grep -q "dangling_image_id" && \
   ! echo "$OUTPUT" | grep -q "Removed container" && \
   ! echo "$OUTPUT" | grep -q "Removed image"; then
    echo "Test 1 PASSED"
else
    echo "Test 1 FAILED"
    echo "Output:" && echo "$OUTPUT"
    exit 1
fi

# --- Test 2: Actual run, should remove old container and dangling image ---
echo "--- Test 2: Actual run (should remove old container and dangling image) ---"
OUTPUT=$(./src/temporal_janitor.sh --days-old 30)
if echo "$OUTPUT" | grep -q "Removed container container_id_old" && \
   echo "$OUTPUT" | grep -q "Removed image dangling_image_id"; then
    echo "Test 2 PASSED"
else
    echo "Test 2 FAILED"
    echo "Output:" && echo "$OUTPUT"
    exit 1
fi

# --- Test 3: Actual run with --days-old 1 (should remove nothing) ---
echo "--- Test 3: Actual run with --days-old 1 (should remove nothing) ---"
OUTPUT=$(./src/temporal_janitor.sh --days-old 1)
if ! echo "$OUTPUT" | grep -q "Removed container" && \
   ! echo "$OUTPUT" | grep -q "Removed image"; then
    echo "Test 3 PASSED"
else
    echo "Test 3 FAILED"
    echo "Output:" && echo "$OUTPUT"
    exit 1
fi

# --- Test 4: Actual run with --force (should include -f in rm/rmi commands) ---
# This test requires a more sophisticated mock to verify arguments passed to rm/rmi.
# For simplicity, we'll just check if the removal messages appear.
# A more advanced mock could log calls and verify them.

echo "--- Test 4: Actual run with --force (should remove old container and dangling image) ---"
OUTPUT=$(./src/temporal_janitor.sh --days-old 30 --force)
if echo "$OUTPUT" | grep -q "Removed container container_id_old" && \
   echo "$OUTPUT" | grep -q "Removed image dangling_image_id"; then
    echo "Test 4 PASSED"
else
    echo "Test 4 FAILED"
    echo "Output:" && echo "$OUTPUT"
    exit 1
fi


echo "All tests completed successfully!"

# Clean up the mock binary directory
rm -rf "$MOCK_BIN_DIR"
