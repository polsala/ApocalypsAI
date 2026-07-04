#!/bin/bash

# Mock rationale: We cannot run actual docker commands in a CI/CD environment
# without a running docker daemon and potentially modifying the host system.
# This mock simulates the output and behavior of key docker commands.

# Store original docker path (not strictly needed if we prepend, but good practice)
# ORIGINAL_DOCKER_PATH=$(which docker)

MOCK_DOCKER_SCRIPT="/tmp/mock_docker.sh"
MOCK_DOCKER_LOG="/tmp/docker_calls.log"

# Create a mock docker executable
cat << 'EOF' > "$MOCK_DOCKER_SCRIPT"
#!/bin/bash
echo "MOCKED_DOCKER_CALL: $@" >> "$MOCK_DOCKER_LOG"
if [[ "$@" == "system prune --force" ]]; then
    echo "Total reclaimed space: 370MB"
elif [[ "$@" == "system prune" ]]; then
    echo -e "WARNING! This will remove:\n  - all stopped containers\n  - all dangling images\n  - all dangling build cache\nAre you sure you want to continue? [y/N] "
else
    echo "Mocked docker command: $@"
fi
EOF
chmod +x "$MOCK_DOCKER_SCRIPT"

# Prepend mock_docker_script's directory to PATH for tests
export PATH="$(dirname "$MOCK_DOCKER_SCRIPT"):$PATH"

# Cleanup function to run at exit
cleanup() {
    rm -f "$MOCK_DOCKER_SCRIPT"
    rm -f "$MOCK_DOCKER_LOG"
}
trap cleanup EXIT

# Ensure log file is clean before each test
cleanup_log() {
    > "$MOCK_DOCKER_LOG"
}

# Test function
run_test() {
    local test_name="$1"
    local command_args="$2"
    local expected_output_regex="$3"
    local expected_mock_calls_regex="$4"

    cleanup_log
    echo "--- Running Test: $test_name ---"
    
    local ACTUAL_OUTPUT
    local ACTUAL_MOCK_CALLS

    # Run the cleanup script and capture output
    if [[ "$command_args" == *"--force"* ]]; then
        ACTUAL_OUTPUT=$(bash src/cleanup.sh $command_args)
    else
        # For interactive system prune, we'll simulate a 'N' response to avoid actual pruning in mock
        ACTUAL_OUTPUT=$(echo "N" | bash src/cleanup.sh $command_args)
    fi
    
    # Capture mock docker calls
    ACTUAL_MOCK_CALLS=$(cat "$MOCK_DOCKER_LOG")

    echo "Actual Output:"
    echo "$ACTUAL_OUTPUT"
    echo "Actual Mock Calls:"
    echo "$ACTUAL_MOCK_CALLS"

    if [[ "$ACTUAL_OUTPUT" =~ $expected_output_regex ]]; then
        echo "Output PASSED for $test_name"
    else
        echo "Output FAILED for $test_name"
        echo "Expected regex: $expected_output_regex"
        exit 1
    fi

    if [[ "$ACTUAL_MOCK_CALLS" =~ $expected_mock_calls_regex ]]; then
        echo "Mock Calls PASSED for $test_name"
    else
        echo "Mock Calls FAILED for $test_name"
        echo "Expected regex: $expected_mock_calls_regex"
        exit 1
    fi
    echo ""
}

# Test Case 1: Dry Run
run_test "Dry Run Mode" "--dry-run" \
    "Initiating temporal scan \(Dry Run mode\)\.\.\. No changes will be made\.\nIf this were a real cleanup, the following command would be executed:\ndocker system prune\nSimulated: Would reclaim 100MB from containers, 200MB from images, 50MB from volumes, 20MB from networks\." \
    "^$" # No docker calls should be made in dry run

# Test Case 2: Force Cleanup
run_test "Force Cleanup Mode" "--force" \
    "Engaging temporal cleanup protocols\.\.\.\nForcing the timeline reset! No confirmation needed\.\nTotal reclaimed space: 370MB" \
    "MOCKED_DOCKER_CALL: system prune --force"

# Test Case 3: Interactive Cleanup (simulating 'N' response)
run_test "Interactive Cleanup Mode (No confirmation)" "" \
    "Engaging temporal cleanup protocols\.\.\.\nInteractive mode: You will be prompted for confirmation\.\nWARNING! This will remove:" \
    "MOCKED_DOCKER_CALL: system prune"

echo "All tests passed!"
