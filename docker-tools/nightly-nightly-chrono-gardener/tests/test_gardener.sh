#!/bin/bash

# Mock rationale: We need to prevent actual docker commands from running
# and instead capture what would have been executed or simulate their output.
# This function will shadow the real 'docker' command during tests.
docker() {
    echo "MOCKED_DOCKER_CALL: $@" >&2 # Send mock calls to stderr to not pollute stdout for assertions
    # Simulate a successful prune output for testing purposes
    if [[ "$@" == "system prune -f" ]]; then
        echo "Total reclaimed space: 100MB"
    elif [[ "$@" == "system prune -f --volumes" ]]; then
        echo "Total reclaimed space: 500MB (including volumes)"
    fi
    return 0 # Simulate success
}

# Path to the script
SCRIPT_PATH="./src/gardener.sh"

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local dry_run_val="$2"
    local prune_volumes_val="$3"
    shift 3
    local expected_patterns=("$@") # Remaining arguments are expected patterns

    echo "--- Running Test: $test_name ---"
    # Capture both stdout and stderr for analysis
    OUTPUT=$(DRY_RUN="$dry_run_val" PRUNE_VOLUMES="$prune_volumes_val" bash "$SCRIPT_PATH" 2>&1)
    
    local success=true

    echo "Captured Output:"
    echo "$OUTPUT"
    echo "--- End Captured Output ---"

    for pattern in "${expected_patterns[@]}"; do
        if ! echo "$OUTPUT" | grep -qF "$pattern"; then # -F for fixed string matching
            echo "❌ Test Failed: $test_name - Missing pattern: '$pattern'"
            success=false
        fi
    done

    if "$success"; then
        echo "✅ Test Passed: $test_name"
    else
        exit 1
    fi
    echo ""
}

# Test 1: Default Prune (no volumes, not dry run)
run_test "Default Prune" "false" "false" \
    "Sweeping away digital debris..." \
    "Total reclaimed space: 100MB" \
    "Unused volumes will be preserved." \
    "MOCKED_DOCKER_CALL: system prune -f"

# Test 2: Prune with Volumes (not dry run)
run_test "Prune with Volumes" "false" "true" \
    "Sweeping away digital debris..." \
    "Total reclaimed space: 500MB (including volumes)" \
    "Including unused volumes in the pruning process." \
    "MOCKED_DOCKER_CALL: system prune -f --volumes"

# Test 3: Dry Run (no volumes)
run_test "Dry Run" "true" "false" \
    "Performing a dry run. No actual pruning will occur, just a peek at the weeds!" \
    "Would execute: docker system prune -f" \
    "Unused volumes will be preserved." \
    "MOCKED_DOCKER_CALL: system prune -f"

# Test 4: Dry Run with Volumes
run_test "Dry Run with Volumes" "true" "true" \
    "Performing a dry run. No actual pruning will occur, just a peek at the weeds!" \
    "Would execute: docker system prune -f --volumes" \
    "Including unused volumes in the pruning process." \
    "MOCKED_DOCKER_CALL: system prune -f --volumes"

echo "All tests completed successfully."
