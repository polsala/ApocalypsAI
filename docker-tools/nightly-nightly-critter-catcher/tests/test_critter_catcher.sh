#!/bin/bash

# Mock rationale:
# The `docker` command is external and interacts with the host system.
# For deterministic and offline testing, we must mock `docker` to control its output
# and simulate its side effects without actually running Docker commands.

# --- Test Setup ---
# Save original docker command
DOCKER_CMD=$(which docker)
CRITTER_CATCHER_SCRIPT="./src/critter_catcher.sh"

# Function to run a test case
run_test() {
    local test_name="$1"
    local expected_output_file="$2"
    local input_response="$3" # 'y' or 'n' for interactive prompts
    local command_arg="$4" # 'scan' or 'cleanup'

    echo "--- Running Test: $test_name ---"

    # Capture stdout and stderr
    # Use a temporary file for stdin simulation
    local temp_stdin=$(mktemp)
    echo "$input_response" > "$temp_stdin"

    # Run the script with mocked docker and capture output
    local actual_output=$(cat "$temp_stdin" | bash "$CRITTER_CATCHER_SCRIPT" "$command_arg" 2>&1)
    local exit_code=$?

    # Clean up temporary stdin file
    rm "$temp_stdin"

    # Compare actual output with expected output
    if diff -u <(echo "$actual_output") "$expected_output_file"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Actual output:"
        echo "$actual_output"
        echo "Expected output (from $expected_output_file):"
        cat "$expected_output_file"
        exit 1
    fi
    echo
}

# --- Mock Docker Command ---
# This function replaces the actual 'docker' command during tests.
# It simulates various docker commands based on arguments.
docker() {
    local cmd="$1"
    local subcmd="$2"
    local args="${@:3}"

    case "$cmd $subcmd" in
        "ps -aq")
            # Mock rationale: Simulate finding stopped containers.
            # This output is used by find_stopped_containers.
            if [[ "$args" == *"-f status=exited"* ]]; then
                echo "a1b2c3d4e5f6"
                echo "f6e5d4c3b2a1"
            fi
            ;;
        "images -f")
            # Mock rationale: Simulate finding dangling images.
            # This output is used by find_dangling_images.
            if [[ "$args" == *"dangling=true -q"* ]]; then
                echo "789abcdef012"
            fi
            ;;
        "volume ls")
            # Mock rationale: Simulate finding unused volumes.
            # This output is used by find_unused_volumes.
            if [[ "$args" == *"-qf dangling=true"* ]]; then
                # Simulate no unused volumes for most tests, or specific ones
                if [[ "$MOCK_VOLUMES" == "true" ]]; then
                    echo "vol_alpha"
                    echo "vol_beta"
                fi
            fi
            ;;
        "inspect --format")
            # Mock rationale: Simulate getting container info.
            # This output is used by get_container_info.
            if [[ "$args" == *"a1b2c3d4e5f6"* ]]; then
                echo "/my-old-app (ubuntu:latest)"
            elif [[ "$args" == *"f6e5d4c3b2a1"* ]]; then
                echo "/dev-db-test (postgres:13)"
            else
                echo "" # No info for unknown IDs
            fi
            ;;
        "images --format")
            # Mock rationale: Simulate getting image info.
            # This output is used by get_image_info.
            if [[ "$args" == *"789abcdef012"* ]]; then
                echo "<none>:<none> (Image ID: 789abcdef012)"
            else
                echo "" # No info for unknown IDs
            fi
            ;;
        "rm a1b2c3d4e5f6")
            # Mock rationale: Simulate successful container removal.
            # This is called when user accepts cleanup.
            echo "" # Silent success
            ;;
        "rm f6e5d4c3b2a1")
            # Mock rationale: Simulate successful container removal.
            echo "" # Silent success
            ;;
        "rmi 789abcdef012")
            # Mock rationale: Simulate successful image removal.
            echo "" # Silent success
            ;;
        "volume rm vol_alpha")
            # Mock rationale: Simulate successful volume removal.
            echo "" # Silent success
            ;;
        "volume rm vol_beta")
            # Mock rationale: Simulate successful volume removal.
            echo "" # Silent success
            ;;
        *)
            # Mock rationale: Catch any unmocked docker commands to prevent actual execution.
            echo "MOCKED DOCKER ERROR: Unhandled command: $@" >&2
            exit 1
            ;;
    esac
}

# Override the 'docker' command with our mock function
export -f docker

# --- Test Cases ---

# Test 1: No critters found (scan mode)
# Expected output: Only welcome, scanning, and no critters message.
cat << 'EOF' > tests/expected_output_no_critters_scan.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 0 Sleepy Critters (stopped containers).

Found 0 Lost Pups (dangling images).

Found 0 Forgotten Nests (unused volumes).

No critters found! Your Docker environment is sparkling clean.
EOF
run_test "No Critters (Scan)" tests/expected_output_no_critters_scan.txt "" "scan"

# Test 2: Critters found, user declines cleanup (cleanup mode)
# Expected output: Critters listed, then skipping message.
cat << 'EOF' > tests/expected_output_critters_decline.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))
  - f6e5d4c3b2a1 (/dev-db-test (postgres:13))

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 0 Forgotten Nests (unused volumes).

Would you like to rehome these critters? (y/N): 
Skipping cleanup. Critters get to stay for now!
EOF
run_test "Critters Found, Decline Cleanup" tests/expected_output_critters_decline.txt "n" "cleanup"

# Test 3: Critters found, user accepts cleanup (cleanup mode)
# Expected output: Critters listed, then rehoming messages, then all rehomed message.
cat << 'EOF' > tests/expected_output_critters_accept.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))
  - f6e5d4c3b2a1 (/dev-db-test (postgres:13))

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 0 Forgotten Nests (unused volumes).

Would you like to rehome these critters? (y/N): 
Rehoming Sleepy Critter a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))...
Rehoming Sleepy Critter f6e5d4c3b2a1 (/dev-db-test (postgres:13))...
Rehoming Lost Pup <none>:<none> (Image ID: 789abcdef012)...

All identified critters have been rehomed. Your Docker environment is now a bit tidier!
EOF
run_test "Critters Found, Accept Cleanup" tests/expected_output_critters_accept.txt "y" "cleanup"

# Test 4: Critters found, scan mode (no prompt)
# Expected output: Critters listed, but no prompt or cleanup messages.
cat << 'EOF' > tests/expected_output_critters_scan.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))
  - f6e5d4c3b2a1 (/dev-db-test (postgres:13))

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 0 Forgotten Nests (unused volumes).
EOF
run_test "Critters Found (Scan Only)" tests/expected_output_critters_scan.txt "" "scan"

# Test 5: Invalid command
cat << 'EOF' > tests/expected_output_invalid_command.txt
Invalid command. Usage: critter_catcher.sh [scan|cleanup]
EOF
run_test "Invalid Command" tests/expected_output_invalid_command.txt "" "invalid"

# Test 6: Default command (no arg) should be cleanup
cat << 'EOF' > tests/expected_output_default_cleanup_decline.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))
  - f6e5d4c3b2a1 (/dev-db-test (postgres:13))

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 0 Forgotten Nests (unused volumes).

Would you like to rehome these critters? (y/N): 
Skipping cleanup. Critters get to stay for now!
EOF
run_test "Default Command (Cleanup, Decline)" tests/expected_output_default_cleanup_decline.txt "n" ""

# Test 7: With volumes, accept cleanup
# Temporarily enable volume mocking
MOCK_VOLUMES="true"
cat << 'EOF' > tests/expected_output_volumes_accept.txt
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))
  - f6e5d4c3b2a1 (/dev-db-test (postgres:13))

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 2 Forgotten Nests (unused volumes):
  - vol_alpha
  - vol_beta

Would you like to rehome these critters? (y/N): 
Rehoming Sleepy Critter a1b2c3d4e5f6 (/my-old-app (ubuntu:latest))...
Rehoming Sleepy Critter f6e5d4c3b2a1 (/dev-db-test (postgres:13))...
Rehoming Lost Pup <none>:<none> (Image ID: 789abcdef012)...
Rehoming Forgotten Nest vol_alpha...
Rehoming Forgotten Nest vol_beta...

All identified critters have been rehomed. Your Docker environment is now a bit tidier!
EOF
run_test "Critters + Volumes Found, Accept Cleanup" tests/expected_output_volumes_accept.txt "y" "cleanup"
unset MOCK_VOLUMES # Disable volume mocking

echo "All tests completed."

# Clean up expected output files
rm tests/expected_output_no_critters_scan.txt
rm tests/expected_output_critters_decline.txt
rm tests/expected_output_critters_accept.txt
rm tests/expected_output_critters_scan.txt
rm tests/expected_output_invalid_command.txt
rm tests/expected_output_default_cleanup_decline.txt
rm tests/expected_output_volumes_accept.txt
