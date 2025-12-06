#!/bin/bash

# Mock rationale: We need to simulate docker command outputs without actually running docker,
# as tests must be deterministic and offline. This mock function replaces the actual 'docker' command.
mock_docker() {
    case "$1 $2 $3 $4 $5 $6 $7 $8 $9" in
        "images -f dangling=true")
            echo -e "REPOSITORY\tTAG\tIMAGE ID\tCREATED\tSIZE\n<none>\t<none>\timg1_id\t2 days ago\t100MB\n<none>\t<none>\timg2_id\t5 days ago\t50MB"
            ;;
        "ps -a -f status=exited")
            echo -e "CONTAINER ID\tIMAGE\tCOMMAND\tCREATED\tSTATUS\tPORTS\tNAMES\ncont1_id\tubuntu\t\"bash\"\t3 days ago\tExited (0)\t\told_container_1\ncont2_id\talpine\t\"sh\"\t7 days ago\tExited (0)\t\told_container_2"
            ;;
        "volume ls -f dangling=true")
            echo -e "DRIVER\tVOLUME NAME\nlocal\tvol1_name\nlocal\tvol2_name"
            ;;
        "builder prune --dry-run") # This is a mock for the dry-run output, not an actual docker command
            echo "  (Running 'docker builder prune' would reclaim space from build cache.)"
            ;;
        "image prune --force")
            echo "Total reclaimed space: 150MB (images)"
            ;;
        "container prune --force")
            echo "Total reclaimed space: 20MB (containers)"
            ;;
        "volume prune --force")
            echo "Total reclaimed space: 50MB (volumes)"
            ;;
        "builder prune --force")
            echo "Total reclaimed space: 300MB (build cache)"
            ;;
        "system prune --force --volumes --all")
            echo "Total reclaimed space: 520MB"
            ;;
        *) # Catch-all for unexpected commands
            echo "Error: Unknown docker command in mock: $*" >&2
            exit 1
            ;;
    esac
}

# Override the docker command for testing by exporting DOCKER_CMD
export DOCKER_CMD="mock_docker"

# Test cases

test_dry_run_all() {
    echo "Running test_dry_run_all..."
    output=$(bash src/weeder.sh --dry-run --all)
    if echo "$output" | grep -q "-- Dangling Images --" && \
       echo "$output" | grep -q "img1_id" && \
       echo "$output" | grep -q "-- Stopped Containers --" && \
       echo "$output" | grep -q "cont1_id" && \
       echo "$output" | grep -q "-- Unused Volumes --" && \
       echo "$output" | grep -q "vol1_name" && \
       echo "$output" | grep -q "-- Build Cache (approximate) --" && \
       echo "$output" | grep -q "Dry run complete. No resources were removed."; then
        echo "test_dry_run_all PASSED"
    else
        echo "test_dry_run_all FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_force_prune_all() {
    echo "Running test_force_prune_all..."
    # Since --force is used, no user input is required.
    output=$(bash src/weeder.sh --force --all)
    if echo "$output" | grep -q "Wasteland weeded!" && \
       echo "$output" | grep -q "Total reclaimed space: 520MB"; then
        echo "test_force_prune_all PASSED"
    else
        echo "test_force_prune_all FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_force_prune_images() {
    echo "Running test_force_prune_images..."
    output=$(bash src/weeder.sh --force --images)
    if echo "$output" | grep -q "Pruning dangling images..." && \
       echo "$output" | grep -q "Total reclaimed space: 150MB (images)" && \
       echo "$output" | grep -q "Wasteland weeded!"; then
        echo "test_force_prune_images PASSED"
    else
        echo "test_force_prune_images FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_force_prune_containers() {
    echo "Running test_force_prune_containers..."
    output=$(bash src/weeder.sh --force --containers)
    if echo "$output" | grep -q "Pruning stopped containers..." && \
       echo "$output" | grep -q "Total reclaimed space: 20MB (containers)" && \
       echo "$output" | grep -q "Wasteland weeded!"; then
        echo "test_force_prune_containers PASSED"
    else
        echo "test_force_prune_containers FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_force_prune_volumes() {
    echo "Running test_force_prune_volumes..."
    output=$(bash src/weeder.sh --force --volumes)
    if echo "$output" | grep -q "Pruning unused volumes..." && \
       echo "$output" | grep -q "Total reclaimed space: 50MB (volumes)" && \
       echo "$output" | grep -q "Wasteland weeded!"; then
        echo "test_force_prune_volumes PASSED"
    else
        echo "test_force_prune_volumes FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_force_prune_build_cache() {
    echo "Running test_force_prune_build_cache..."
    output=$(bash src/weeder.sh --force --build-cache)
    if echo "$output" | grep -q "Pruning build cache..." && \
       echo "$output" | grep -q "Total reclaimed space: 300MB (build cache)" && \
       echo "$output" | grep -q "Wasteland weeded!"; then
        echo "test_force_prune_build_cache PASSED"
    else
        echo "test_force_prune_build_cache FAILED"
        echo "Output: $output"
        exit 1
    fi
}

test_no_force_prune_abort() {
    echo "Running test_no_force_prune_abort..."
    # Mock rationale: Simulate user input 'n' to abort the pruning.
    # We use 'echo "n" |' to pipe 'n' as input to the script's read command.
    output=$(echo "n" | bash src/weeder.sh --all 2>&1)
    if echo "$output" | grep -q "Aborting." && \
       ! echo "$output" | grep -q "Wasteland weeded!"; then
        echo "test_no_force_prune_abort PASSED"
    else
        echo "test_no_force_prune_abort FAILED"
        echo "Output: $output"
        exit 1
    fi
}

# Run all tests
test_dry_run_all
test_force_prune_all
test_force_prune_images
test_force_prune_containers
test_force_prune_volumes
test_force_prune_build_cache
test_no_force_prune_abort

echo "All tests completed."
