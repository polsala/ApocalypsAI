#!/bin/bash

# Mock rationale: The 'docker' command interacts with the Docker daemon,
# which is an external dependency. To ensure deterministic and offline tests,
# we mock the 'docker' command to return predefined outputs for specific
# subcommands. This allows us to simulate different Docker environment states
# without actually running a Docker daemon or modifying a real one.

# --- Mock Docker Command ---
MOCKED_DOCKER_OUTPUT_IMAGES=""
MOCKED_DOCKER_OUTPUT_VOLUMES=""
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE=""

docker() {
    local cmd="$1"
    local subcmd="$2"
    local filter_arg="$3"

    case "$cmd $subcmd $filter_arg" in
        "docker images -f dangling=true")
            echo "$MOCKED_DOCKER_OUTPUT_IMAGES"
            ;;
        "docker volume ls -f dangling=true")
            echo "$MOCKED_DOCKER_OUTPUT_VOLUMES"
            ;;
        "docker network prune --force --dry-run")
            echo "$MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE"
            ;;
        *)
            echo "Error: Unexpected docker command in mock: $@" >&2
            exit 1
            ;;
    esac
}

# --- Test Helper Functions ---
assert_contains() {
    local expected_regex="$1" # Now expects a regex
    local actual="$2"
    local test_name="$3"
    if echo "$actual" | grep -qE "$expected_regex"; then # Use -E for extended regex
        echo "✅ PASS: $test_name (contains regex '$expected_regex')"
    else
        echo "❌ FAIL: $test_name (expected to contain regex '$expected_regex', but got:\n$actual)"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected_regex="$1" # Now expects a regex
    local actual="$2"
    local test_name="$3"
    if echo "$actual" | grep -qE "$unexpected_regex"; then # Use -E for extended regex
        echo "❌ FAIL: $test_name (expected NOT to contain regex '$unexpected_regex', but got:\n$actual)"
        exit 1
    else
        echo "✅ PASS: $test_name (does not contain regex '$unexpected_regex')"
    fi
}

run_test() {
    local test_name="$1"
    shift
    local -a expected_output_contains=()
    local -a expected_output_not_contains=()

    # Parse arguments: first array is contains, second is not_contains
    local parsing_contains=true
    for arg in "$@"; do
        if [[ "$arg" == "--not-contains" ]]; then
            parsing_contains=false
            continue
        fi
        if "$parsing_contains"; then
            expected_output_contains+=("$arg")
        else
            expected_output_not_contains+=("$arg")
        fi
    done

    echo "--- Running Test: $test_name ---"

    OUTPUT=$(bash src/dust_bunny_sweeper.sh)

    for expected in "${expected_output_contains[@]}"; do
        assert_contains "$expected" "$OUTPUT" "$test_name"
    done

    for unexpected in "${expected_output_not_contains[@]}"; do
        assert_not_contains "$unexpected" "$OUTPUT" "$test_name"
    done
    echo ""
}

# --- Test Cases ---

# Test Case 1: No dust bunnies
MOCKED_DOCKER_OUTPUT_IMAGES=""
MOCKED_DOCKER_OUTPUT_VOLUMES=""
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE="Total reclaimed space: 0B"
run_test "No Dust Bunnies Found" \
    "Your image registry is sparkling clean! No dangling images found." \
    "All your data volumes are neatly organized! No unused volumes found." \
    "Your network pathways are clear! No unused networks found." \
    "--not-contains" \
    "Found [0-9]+ digital dust bunnies" \
    "Discovered [0-9]+ forgotten data clumps!" \
    "Found [0-9]+ tangled network threads!"

# Test Case 2: With dangling images
MOCKED_DOCKER_OUTPUT_IMAGES="sha256:image1id\nsha256:image2id"
MOCKED_DOCKER_OUTPUT_VOLUMES=""
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE="Total reclaimed space: 0B"
run_test "Dangling Images Found" \
    "Found 2 digital dust bunnies in your image collection!" \
    "Your image registry is sparkling clean! No dangling images found." \
    "All your data volumes are neatly organized! No unused volumes found." \
    "Your network pathways are clear! No unused networks found." \
    "--not-contains" \
    "Discovered [0-9]+ forgotten data clumps!" \
    "Found [0-9]+ tangled network threads!"

# Test Case 3: With unused volumes
MOCKED_DOCKER_OUTPUT_IMAGES=""
MOCKED_DOCKER_OUTPUT_VOLUMES="volume1\nvolume2\nvolume3"
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE="Total reclaimed space: 0B"
run_test "Unused Volumes Found" \
    "Your image registry is sparkling clean! No dangling images found." \
    "Discovered 3 forgotten data clumps!" \
    "All your data volumes are neatly organized! No unused volumes found." \
    "Your network pathways are clear! No unused networks found." \
    "--not-contains" \
    "Found [0-9]+ digital dust bunnies" \
    "Found [0-9]+ tangled network threads!"

# Test Case 4: With unused networks
MOCKED_DOCKER_OUTPUT_IMAGES=""
MOCKED_DOCKER_OUTPUT_VOLUMES=""
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE="\nWould delete network 1a2b3c4d5e6f (my_old_net)\nWould delete network f6e5d4c3b2a1 (another_unused_net)\nTotal reclaimed space: 100B\n"
run_test "Unused Networks Found" \
    "Your image registry is sparkling clean! No dangling images found." \
    "All your data volumes are neatly organized! No unused volumes found." \
    "Found 2 tangled network threads!" \
    "--not-contains" \
    "Found [0-9]+ digital dust bunnies" \
    "Discovered [0-9]+ forgotten data clumps!" \
    "Your network pathways are clear! No unused networks found."

# Test Case 5: All types of dust bunnies
MOCKED_DOCKER_OUTPUT_IMAGES="sha256:imageA\nsha256:imageB"
MOCKED_DOCKER_OUTPUT_VOLUMES="vol_alpha\nvol_beta"
MOCKED_DOCKER_OUTPUT_NETWORKS_PRUNE="\nWould delete network net_id_1 (net_name_1)\nTotal reclaimed space: 50B\n"
run_test "All Dust Bunnies Found" \
    "Found 2 digital dust bunnies in your image collection!" \
    "Discovered 2 forgotten data clumps!" \
    "Found 1 tangled network threads!" \
    "--not-contains" \
    "Your image registry is sparkling clean! No dangling images found." \
    "All your data volumes are neatly organized! No unused volumes found." \
    "Your network pathways are clear! No unused networks found."

echo "All tests completed."
