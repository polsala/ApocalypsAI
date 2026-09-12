#!/bin/bash

set -euo pipefail

# Mock rationale: To make tests deterministic and offline, we mock the 'docker' CLI command.
# This avoids requiring a live Docker daemon and ensures consistent test results.

mock_docker() {
    local subcommand="$1"
    shift # Remove the subcommand from arguments

    case "$subcommand" in
        "ps")
            if [[ "$*" == "-a --filter status=exited --format {{.ID}}\t{{.Status}}\t{{.Names}}" ]]; then
                # Simulate one exited container and one running container
                echo -e "c1234567890a\tExited (0) 2 hours ago\tstale_app_container\n" \
                        "c234567890ab\tUp 10 minutes\trunning_app_container"
            else
                echo "Error: Unexpected docker ps arguments: $*" >&2
                return 1
            fi
            ;;
        "images")
            if [[ "$*" == "--filter dangling=true --format {{.ID}}\t{{.Repository}}\t{{.Tag}}" ]]; then
                # Simulate one dangling image and one used image
                echo -e "i1234567890a\t<none>\t<none>\n" \
                        "i234567890ab\tmy-app\tlatest"
            else
                echo "Error: Unexpected docker images arguments: $*" >&2
                return 1
            fi
            ;;
        "volume")
            if [[ "$*" == "ls --filter dangling=true --format {{.Name}}" ]]; then
                # Simulate one dangling volume and one used volume
                echo -e "old_data_volume\n" \
                        "active_data_volume"
            else
                echo "Error: Unexpected docker volume ls arguments: $*" >&2
                return 1
            fi
            ;;
        "system")
            if [[ "$*" == "prune --all --force --volumes" ]]; then
                echo "Total reclaimed space: 100MB"
            else
                echo "Error: Unexpected docker system prune arguments: $*" >&2
                return 1
            fi
            ;;
        *)
            echo "Error: Unknown docker subcommand: $subcommand" >&2
            return 1
            ;;
    esac
}

# Override the 'docker' command with our mock function for testing
docker() { mock_docker "$@"; }

# --- Test Cases ---

# Test 1: Dry Run - Stale resources found
echo "Running Test 1: Dry Run with stale resources..."
OUTPUT=$(bash src/compost_collector.sh --dry-run)

if echo "$OUTPUT" | grep -q "Found 1 exited container(s) ready for composting:" && \
   echo "$OUTPUT" | grep -q "Found 1 dangling image(s) for decomposition:" && \
   echo "$OUTPUT" | grep -q "Found 1 unused volume(s) to return to the earth:" && \
   echo "$OUTPUT" | grep -q "This was a dry run. No resources were composted."; then
    echo "Test 1 PASSED: Dry run correctly identified stale resources and reported no pruning."
else
    echo "Test 1 FAILED: Dry run did not behave as expected."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 2: Force Run - Stale resources found and pruned
echo "\nRunning Test 2: Force Run with stale resources..."
OUTPUT=$(bash src/compost_collector.sh --force)

if echo "$OUTPUT" | grep -q "Found 1 exited container(s) ready for composting:" && \
   echo "$OUTPUT" | grep -q "Initiating digital decomposition..." && \
   echo "$OUTPUT" | grep -q "Total reclaimed space: 100MB" && \
   echo "$OUTPUT" | grep -q "Composting complete! Your digital garden is refreshed."; then
    echo "Test 2 PASSED: Force run correctly identified, pruned, and reported success."
else
    echo "Test 2 FAILED: Force run did not behave as expected."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 3: Default behavior (Dry Run) - No stale resources
echo "\nRunning Test 3: Default (Dry Run) with no stale resources..."

# Temporarily modify mock_docker to return no stale resources
mock_docker_no_stale() {
    local subcommand="$1"
    shift
    case "$subcommand" in
        "ps")
            echo -e "c234567890ab\tUp 10 minutes\trunning_app_container"
            ;;
        "images")
            echo -e "i234567890ab\tmy-app\tlatest"
            ;;
        "volume")
            echo -e "active_data_volume"
            ;;
        "system")
            echo "Total reclaimed space: 0MB"
            ;;
        *)
            mock_docker "$subcommand" "$@"
            ;;
    esac
}
docker() { mock_docker_no_stale "$@"; }

OUTPUT=$(bash src/compost_collector.sh)

if echo "$OUTPUT" | grep -q "No exited containers found." && \
   echo "$OUTPUT" | grep -q "No dangling images found." && \
   echo "$OUTPUT" | grep -q "No unused volumes found." && \
   echo "$OUTPUT" | grep -q "No digital detritus found. Your garden is already sparkling clean!"; then
    echo "Test 3 PASSED: Default dry run correctly reported no stale resources."
else
    echo "Test 3 FAILED: Default dry run with no stale resources did not behave as expected."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

echo "\nAll tests passed!"
