#!/bin/bash

# Nightly Docker Dust Sweeper - tests/test_sweep.sh

set -euo pipefail

# --- Test Setup ---

# Mock rationale: We need to test the script's logic without actually interacting with a Docker daemon.
# This mock simulates the output of 'docker system prune' and other docker commands,
# and prevents actual resource deletion during testing.

MOCK_DOCKER_DIR=$(mktemp -d)
export PATH="$MOCK_DOCKER_DIR:$PATH"
MOCK_LOG="$MOCK_DOCKER_DIR/docker_calls.log"

# Create a mock 'docker' command executable
cat << 'EOF' > "$MOCK_DOCKER_DIR/docker"
#!/bin/bash
echo "MOCK_DOCKER_CALL: $@" >> "$MOCK_LOG"

case "$1" in
    system)
        if [[ "$2" == "prune" ]]; then
            echo "Total reclaimed space: 100MB"
            echo "Total reclaimed volumes: 2"
            echo "Total reclaimed images: 3"
            echo "Total reclaimed networks: 1"
            exit 0
        fi
        ;;
    ps)
        if [[ "$3" == "-a" ]]; then
            echo "CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES"
            echo "a1b2c3d4e5f6        nginx:latest        \"nginx -g 'daemon \" 2 hours ago         Up 2 hours          80/tcp              webserver"
            echo "b2c3d4e5f6a1        ubuntu:latest       \"bash\"              3 days ago          Exited (0) 2 days ago                       old_container"
        fi
        exit 0
        ;;
    images)
        if [[ "$3" == "-f" && "$4" == "dangling=true" ]]; then
            echo "REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE"
            echo "nginx               latest              abc123def456        2 hours ago         100MB"
            echo "<none>              <none>              def789abc012        3 days ago          50MB"
        fi
        exit 0
        ;;
    volume)
        if [[ "$2" == "ls" ]]; then
            echo "DRIVER              VOLUME NAME"
            echo "local               my_volume"
            echo "local               another_volume"
        fi
        exit 0
        ;;
    network)
        if [[ "$2" == "ls" ]]; then
            echo "NETWORK ID          NAME                DRIVER              SCOPE"
            echo "a1b2c3d4e5          bridge              bridge              local"
            echo "f6g7h8i9j0          my_network          bridge              local"
        fi
        exit 0
        ;;
esac

echo "Unknown mock docker command: $@" >&2
exit 1
EOF
chmod +x "$MOCK_DOCKER_DIR/docker"

# Source the script to be tested (relative path)
SCRIPT_TO_TEST="$(dirname "$0")/../src/sweep.sh"

# Helper for consistent test output
log_info() { echo -e "ℹ️ \033[0;34m$1\033[0m"; }

# --- Test Cases ---

# Test 1: Dry run functionality
echo "--- Running Dry Run Test ---"
rm -f "$MOCK_LOG" # Clear log for this test
OUTPUT_DRY_RUN=$("$SCRIPT_TO_TEST" --dry-run 2>&1)

if ! echo "$OUTPUT_DRY_RUN" | grep -q "Dry run enabled"; then
    echo "FAIL: Dry run message not found."
    echo "Output: $OUTPUT_DRY_RUN"
    exit 1
fi

if grep -q "MOCK_DOCKER_CALL: system prune" "$MOCK_LOG"; then
    echo "FAIL: 'docker system prune' was called during dry run."
    cat "$MOCK_LOG"
    exit 1
fi

if ! echo "$OUTPUT_DRY_RUN" | grep -q "Container (exited): old_container (ubuntu:latest)"; then
    echo "FAIL: Expected exited container not listed in dry run."
    echo "Output: $OUTPUT_DRY_RUN"
    exit 1
fi

if ! echo "$OUTPUT_DRY_RUN" | grep -q "Dangling Image: <none>:<none> (ID: def789abc012)"; then
    echo "FAIL: Expected dangling image not listed in dry run."
    echo "Output: $OUTPUT_DRY_RUN"
    exit 1
fi

if ! echo "$OUTPUT_DRY_RUN" | grep -q "Dangling Volume: my_volume"; then
    echo "FAIL: Expected dangling volume not listed in dry run."
    echo "Output: $OUTPUT_DRY_RUN"
    exit 1
fi

if ! echo "$OUTPUT_DRY_RUN" | grep -q "Potentially Unused Network: my_network"; then
    echo "FAIL: Expected potentially unused network not listed in dry run."
    echo "Output: $OUTPUT_DRY_RUN"
    exit 1
fi

log_info "PASS: Dry run test completed successfully."

# Test 2: Actual sweep functionality
echo "\n--- Running Actual Sweep Test ---"
rm -f "$MOCK_LOG" # Clear log for this test
OUTPUT_SWEEP=$("$SCRIPT_TO_TEST" 2>&1)

if ! echo "$OUTPUT_SWEEP" | grep -q "Sweeping away the digital dust bunnies!"; then
    echo "FAIL: Sweep start message not found."
    echo "Output: $OUTPUT_SWEEP"
    exit 1
fi

if ! grep -q "MOCK_DOCKER_CALL: system prune -f --volumes" "$MOCK_LOG"; then
    echo "FAIL: 'docker system prune -f --volumes' was not called."
    cat "$MOCK_LOG"
    exit 1
fi

if ! echo "$OUTPUT_SWEEP" | grep -q "Total reclaimed space: 100MB"; then
    echo "FAIL: Reclaimed space not reported."
    echo "Output: $OUTPUT_SWEEP"
    exit 1
fi

if ! echo "$OUTPUT_SWEEP" | grep -q "Your Docker-verse is sparkling clean!"; then
    echo "FAIL: Success message not found."
    echo "Output: $OUTPUT_SWEEP"
    exit 1
fi

log_info "PASS: Actual sweep test completed successfully."

# Test 3: Unknown argument
echo "\n--- Running Unknown Argument Test ---"
if OUTPUT_UNKNOWN=$("$SCRIPT_TO_TEST" --bad-arg 2>&1); then
    echo "FAIL: Script did not exit with error for unknown argument."
    echo "Output: $OUTPUT_UNKNOWN"
    exit 1
fi
if ! echo "$OUTPUT_UNKNOWN" | grep -q "Unknown argument: --bad-arg"; then
    echo "FAIL: Expected error message for unknown argument not found."
    echo "Output: $OUTPUT_UNKNOWN"
    exit 1
fi
log_info "PASS: Unknown argument test completed successfully."

# --- Cleanup ---
cleanup() {
    rm -rf "$MOCK_DOCKER_DIR"
}
trap cleanup EXIT

echo "\n✅ \033[0;32mAll Nightly Docker Dust Sweeper tests passed!\033[0m"
