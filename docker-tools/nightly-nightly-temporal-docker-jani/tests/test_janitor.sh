#!/bin/sh

# Mock rationale: We need to test the script's logic without actually interacting with a Docker daemon.
# This mock captures the 'docker' commands that would be executed and simulates their output.
MOCKED_COMMANDS=""
mock_docker() {
    MOCKED_COMMANDS="${MOCKED_COMMANDS}\n$@"
    # Simulate success for prune commands with minimal output
    case "$1" in
        container|image|volume|network)
            echo "Total reclaimed space: 0B"
            ;;
        *)
            echo "Unknown mocked docker command: $@" >&2
            return 1
            ;;
    esac
}

# Override the actual docker command with our mock
alias docker='mock_docker'

# Path to the script under test
SCRIPT_TO_TEST="./src/janitor.sh"

# Function to run a test case
run_test() {
    TEST_NAME="$1"
    EXPECTED_CONTAINER="$2"
    EXPECTED_IMAGE="$3"
    EXPECTED_ALL_IMAGES="$4"
    EXPECTED_VOLUME="$5"
    EXPECTED_NETWORK="$6"

    echo "--- Test Case: $TEST_NAME ---"
    MOCKED_COMMANDS="" # Reset captured commands

    # Run the script with specific environment variables
    DOCKER_PRUNE_CONTAINERS="$EXPECTED_CONTAINER" \
    DOCKER_PRUNE_IMAGES="$EXPECTED_IMAGE" \
    DOCKER_PRUNE_VOLUMES="$EXPECTED_VOLUME" \
    DOCKER_PRUNE_NETWORKS="$EXPECTED_NETWORK" \
    DOCKER_PRUNE_ALL_IMAGES="$EXPECTED_ALL_IMAGES" \
    "$SCRIPT_TO_TEST" > /dev/null 2>&1

    # Assertions
    if [ "$EXPECTED_CONTAINER" = "true" ]; then
        echo "$MOCKED_COMMANDS" | grep -q "container prune -f" || { echo "FAIL: $TEST_NAME - Did not prune containers"; exit 1; }
    else
        echo "$MOCKED_COMMANDS" | grep -q "container prune -f" && { echo "FAIL: $TEST_NAME - Pruned containers unexpectedly"; exit 1; }
    fi

    if [ "$EXPECTED_IMAGE" = "true" ]; then
        echo "$MOCKED_COMMANDS" | grep -q "image prune -f" || { echo "FAIL: $TEST_NAME - Did not prune dangling images"; exit 1; }
    else
        echo "$MOCKED_COMMANDS" | grep -q "image prune -f" && { echo "FAIL: $TEST_NAME - Pruned dangling images unexpectedly"; exit 1; }
    fi

    if [ "$EXPECTED_ALL_IMAGES" = "true" ]; then
        echo "$MOCKED_COMMANDS" | grep -q "image prune -a -f" || { echo "FAIL: $TEST_NAME - Did not prune all images"; exit 1; }
    else
        echo "$MOCKED_COMMANDS" | grep -q "image prune -a -f" && { echo "FAIL: $TEST_NAME - Pruned all images unexpectedly"; exit 1; }
    fi

    if [ "$EXPECTED_VOLUME" = "true" ]; then
        echo "$MOCKED_COMMANDS" | grep -q "volume prune -f" || { echo "FAIL: $TEST_NAME - Did not prune volumes"; exit 1; }
    else
        echo "$MOCKED_COMMANDS" | grep -q "volume prune -f" && { echo "FAIL: $TEST_NAME - Pruned volumes unexpectedly"; exit 1; }
    fi

    if [ "$EXPECTED_NETWORK" = "true" ]; then
        echo "$MOCKED_COMMANDS" | grep -q "network prune -f" || { echo "FAIL: $TEST_NAME - Did not prune networks"; exit 1; }
    else
        echo "$MOCKED_COMMANDS" | grep -q "network prune -f" && { echo "FAIL: $TEST_NAME - Pruned networks unexpectedly"; exit 1; }
    fi

    echo "PASS: $TEST_NAME"
}

# --- Test Cases ---
# Test 1: Default behavior (prune containers and dangling images)
run_test "Default behavior (containers, dangling images)" true true false false false

# Test 2: Prune everything (containers, dangling images, all images, volumes, networks)
run_test "Prune everything" true true true true true

# Test 3: Prune only volumes
run_test "Prune only volumes" false false false true false

# Test 4: No pruning (all false)
run_test "No pruning" false false false false false

# Test 5: Prune all images only (implies dangling images also pruned)
run_test "Prune all images only" false true true false false

echo "\nAll tests passed!"
