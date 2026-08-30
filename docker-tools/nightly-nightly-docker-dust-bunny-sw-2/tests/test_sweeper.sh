#!/bin/bash
set -euo pipefail

# Mock rationale: We need to test the script's logic without actually interacting
# with a real Docker daemon, which would be non-deterministic and require a live
# Docker environment. Mocking `docker` commands allows us to control their output
# and verify the script's behavior based on different scenarios.

# Create a temporary directory for our mock docker executable
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH"

# --- Mock Docker executable ---
# This function will act as our mock 'docker' command.
# It will simulate different scenarios based on the arguments passed to it.
mock_docker() {
    case "$@" in
        "ps -a -f status=exited -q")
            if [ "$MOCK_SCENARIO" == "no_dust" ]; then
                echo ""
            elif [ "$MOCK_SCENARIO" == "some_dust" ]; then
                echo "container_id_1\ncontainer_id_2"
            fi
            ;;
        "rm container_id_1 container_id_2")
            echo "container_id_1\ncontainer_id_2" # Simulate successful removal
            ;;
        "rm container_id_1") # For single container removal
            echo "container_id_1"
            ;;
        "images -f dangling=true -q")
            if [ "$MOCK_SCENARIO" == "no_dust" ]; then
                echo ""
            elif [ "$MOCK_SCENARIO" == "some_dust" ]; then
                echo "image_id_a\nimage_id_b"
            fi
            ;;
        "rmi image_id_a image_id_b")
            echo "image_id_a\nimage_id_b" # Simulate successful removal
            ;;
        "rmi image_id_a") # For single image removal
            echo "image_id_a"
            ;;
        "volume ls -f dangling=true -q")
            if [ "$MOCK_SCENARIO" == "no_dust" ]; then
                echo ""
            elif [ "$MOCK_SCENARIO" == "some_dust" ]; then
                echo "volume_name_x\nvolume_name_y"
            fi
            ;;
        "volume rm volume_name_x volume_name_y")
            echo "volume_name_x\nvolume_name_y" # Simulate successful removal
            ;;
        "volume rm volume_name_x") # For single volume removal
            echo "volume_name_x"
            ;;
        *)
            echo "Error: Unexpected docker command: $@" >&2
            exit 1
            ;;
    esac
}

# Create the mock docker executable
echo '#!/bin/bash' > "$MOCK_BIN_DIR/docker"
echo 'mock_docker "$@"' >> "$MOCK_BIN_DIR/docker"
chmod +x "$MOCK_BIN_DIR/docker"

# Source the script to be tested
# We need to run it directly, not via docker, for testing the script logic.
# The Dockerfile tests the containerization.
SCRIPT_TO_TEST="./src/dust_bunny_sweeper.sh"

# --- Test Scenarios ---

# Scenario 1: No dust bunnies (nothing to clean)
echo "--- Running Test Scenario 1: No dust bunnies ---"
MOCK_SCENARIO="no_dust"
OUTPUT=$(bash "$SCRIPT_TO_TEST")

echo "$OUTPUT"
if echo "$OUTPUT" | grep -q "No exited containers (dust bunnies) found"; then
    echo "Test 1.1 (no exited containers) PASSED"
else
    echo "Test 1.1 (no exited containers) FAILED"
    exit 1
fi
if echo "$OUTPUT" | grep -q "No dangling images (lint) found"; then
    echo "Test 1.2 (no dangling images) PASSED"
else
    echo "Test 1.2 (no dangling images) FAILED"
    exit 1
fi
if echo "$OUTPUT" | grep -q "No dangling volumes (fluff) found"; then
    echo "Test 1.3 (no dangling volumes) PASSED"
else
    echo "Test 1.3 (no dangling volumes) FAILED"
    exit 1
fi
echo "Scenario 1 PASSED"
echo ""

# Scenario 2: Some dust bunnies (items to clean)
echo "--- Running Test Scenario 2: Some dust bunnies ---"
MOCK_SCENARIO="some_dust"
OUTPUT=$(bash "$SCRIPT_TO_TEST")

echo "$OUTPUT"
if echo "$OUTPUT" | grep -q "Exited containers swept away!"; then
    echo "Test 2.1 (exited containers cleaned) PASSED"
else
    echo "Test 2.1 (exited containers cleaned) FAILED"
    exit 1
fi
if echo "$OUTPUT" | grep -q "Dangling images swept away!"; then
    echo "Test 2.2 (dangling images cleaned) PASSED"
else
    echo "Test 2.2 (dangling images cleaned) FAILED"
    exit 1
fi
if echo "$OUTPUT" | grep -q "Dangling volumes swept away!"; then
    echo "Test 2.3 (dangling volumes cleaned) PASSED"
else
    echo "Test 2.3 (dangling volumes cleaned) FAILED"
    exit 1
fi
echo "Scenario 2 PASSED"
echo ""

# Cleanup mock directory
rm -rf "$MOCK_BIN_DIR"
echo "All tests PASSED!"
