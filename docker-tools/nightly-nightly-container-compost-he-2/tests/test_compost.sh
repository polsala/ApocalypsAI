#!/bin/bash

# Mock rationale: We need to mock the 'docker' command to prevent actual system changes
# and ensure deterministic tests.
# This function will replace the real 'docker' command during tests.
docker() {
    local cmd="$1"
    shift
    case "$cmd" in
        "system")
            local subcmd="$1"
            shift
            case "$subcmd" in
                "prune")
                    local flags="$@"
                    if [[ "$flags" == "--force --volumes" ]]; then
                        echo "Deleted Images:"
                        echo "untagged: old-image:v1"
                        echo "Total reclaimed space: 150MB"
                        return 0
                    else
                        echo "Error: Unexpected prune flags: $flags" >&2
                        return 1
                    fi
                    ;;
                "df")
                    echo "TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE"
                    echo "Images              5                   3                   500MB               200MB"
                    echo "Containers          10                  7                   100MB               30MB"
                    echo "Local Volumes       3                   1                   50MB                20MB"
                    return 0
                    ;;
                *)
                    echo "Error: Unknown docker system subcommand: $subcmd" >&2
                    return 1
                    ;;
            esac
            ;;
        *)
            echo "Error: Unknown docker command: $cmd" >&2
            return 1
            ;;
    esac
}

# Mock rationale: This function simulates 'docker' when no space is reclaimed.
docker_no_space() {
    local cmd="$1"
    shift
    case "$cmd" in
        "system")
            local subcmd="$1"
            shift
            case "$subcmd" in
                "prune")
                    echo "Total reclaimed space: 0B"
                    return 0
                    ;;
                "df")
                    echo "TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE"
                    echo "Images              5                   5                   500MB               0B"
                    echo "Containers          10                  10                  100MB               0B"
                    echo "Local Volumes       3                   3                   50MB                0B"
                    return 0
                    ;;
                *)
                    echo "Error: Unknown docker system subcommand: $subcmd" >&2
                    return 1
                    ;;
            esac
            ;;
        *)
            echo "Error: Unknown docker command: $cmd" >&2
            return 1
            ;;
    esac
}

# Export the mock functions so they are available in subshells (where compost.sh runs)
export -f docker
export -f docker_no_space

# Test 1: Dry run functionality
test_dry_run() {
    echo "Running test_dry_run..."
    # Ensure the default mock_docker is used
    export -f docker # Re-export to ensure it's the primary one if it was overridden
    OUTPUT=$(./src/compost.sh --dry-run)
    if echo "$OUTPUT" | grep -q "Initiating a dry run of the Digital Compost Heap..." && \
       echo "$OUTPUT" | grep -q "Simulating 'docker system df' output for dry run:" && \
       echo "$OUTPUT" | grep -q "approximately 250MB of digital space could be reclaimed." && \
       echo "$OUTPUT" | grep -q "Dry run complete. No actual composting performed."; then
        echo "test_dry_run PASSED"
    else
        echo "test_dry_run FAILED"
        echo "Output was:"
        echo "$OUTPUT"
        exit 1
    fi
}

# Test 2: Actual prune functionality (successful run)
test_prune_success() {
    echo "Running test_prune_success..."
    # Ensure the default mock_docker is used
    export -f docker
    OUTPUT=$(./src/compost.sh)
    if echo "$OUTPUT" | grep -q "Activating the Digital Compost Heap!" && \
       echo "$OUTPUT" | grep -q "Composting in progress..." && \
       echo "$OUTPUT" | grep -q "Total reclaimed space: 150MB" && \
       echo "$OUTPUT" | grep -q "Digital composting complete! We've turned 150MB of digital waste into fresh, usable space."; then
        echo "test_prune_success PASSED"
    else
        echo "test_prune_success FAILED"
        echo "Output was:"
        echo "$OUTPUT"
        exit 1
    fi
}

# Test 3: Prune with no space reclaimed
test_prune_no_space() {
    echo "Running test_prune_no_space..."
    # Mock rationale: Temporarily replace the 'docker' function with 'docker_no_space' for this test.
    # This is done by redefining `docker` function for this test within a subshell.
    (
        docker() { docker_no_space "$@"; }
        export -f docker # Export the locally redefined docker function
        OUTPUT=$(./src/compost.sh)
        if echo "$OUTPUT" | grep -q "Activating the Digital Compost Heap!" && \
           echo "$OUTPUT" | grep -q "Composting in progress..." && \
           echo "$OUTPUT" | grep -q "The digital garden was already pristine! No space to reclaim, but thanks for checking."; then
            echo "test_prune_no_space PASSED"
        else
            echo "test_prune_no_space FAILED"
            echo "Output was:"
            echo "$OUTPUT"
            exit 1
        fi
    )
    # The subshell exits, restoring the original 'docker' function in the parent shell
    if [ $? -ne 0 ]; then exit 1; fi # Propagate failure from subshell
}


# Run all tests
test_dry_run
test_prune_success
test_prune_no_space

echo "All tests completed."
