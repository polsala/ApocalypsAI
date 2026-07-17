#!/bin/bash

# Mock rationale: We need to test the script's output based on various system states
# without actually interacting with the real system or network. Mocking commands
# allows for deterministic and offline testing.

# Define a temporary directory for mocks and test output
TEST_DIR=$(mktemp -d)
export PATH="$TEST_DIR:$PATH" # Add mock directory to PATH

# Create mock commands
create_mock() {
    local cmd_name="$1"
    local output="$2"
    echo -e "#!/bin/bash\n# Mock rationale: Simulates '$cmd_name' command output for testing.\necho -e \"$output\"" > "$TEST_DIR/$cmd_name"
    chmod +x "$TEST_DIR/$cmd_name"
}

# Mock git command for specific scenarios
create_git_mock() {
    local output="$1"
    echo -e "#!/bin/bash\n# Mock rationale: Simulates 'git' command output for testing.\nif [[ \"\$1\" == \"rev-parse\" ]]; then exit 0; else echo -e \"$output\"; fi" > "$TEST_DIR/git"
    chmod +x "$TEST_DIR/git"
}

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Test function
run_test() {
    local test_name="$1"
    local expected_output_file="$2"
    local actual_output_file="$3"

    echo "Running test: $test_name"
    # Run the script and capture its output
    bash ../src/nomad_compass.sh > "$actual_output_file" 2>&1

    # Compare actual output with expected output
    if diff -u "$expected_output_file" "$actual_output_file"; then
        echo "PASS: $test_name"
        return 0
    else
        echo "FAIL: $test_name"
        return 1
    fi
}

# --- Test Case 1: All system info, clean git repo ---
echo "--- Setting up Test Case 1: All system info, clean git repo ---"
create_mock "uptime" "up 1 day, 5 hours, 30 minutes"
create_mock "hostname" "192.168.1.100" # hostname -I output
create_mock "df" "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1       100G   20G   80G  20% /"
create_mock "free" "              total        used        free      shared  buff/cache   available\nMem:           15Gi       4.0Gi       8.0Gi       1.0Gi       3.0Gi        10Gi"
create_mock "pwd" "/home/user/project"
create_git_mock "## main\n" # git status --short --branch output for clean repo

EXPECTED_OUTPUT_1="$TEST_DIR/expected_output_1.txt"
ACTUAL_OUTPUT_1="$TEST_DIR/actual_output_1.txt"

cat <<EOF > "$EXPECTED_OUTPUT_1"

\033[0;36m--- Nightly Digital Nomad's Compass ---\033[0m
\033[0;32mUptime:\033[0m up 1 day, 5 hours, 30 minutes
\033[0;33mIP Address:\033[0m 192.168.1.100
\033[0;34mDisk Usage:\033[0m 20% used of 100G
\033[0;35mMemory Usage:\033[0m 4.0Gi used of 15Gi
\033[0;36mCurrent Path:\033[0m /home/user/project
\033[0;32mGit Status:\033[0m
  ## main
\033[0;36m---------------------------------------\033[0m

EOF

run_test "All system info, clean git repo" "$EXPECTED_OUTPUT_1" "$ACTUAL_OUTPUT_1"
TEST_RESULT_1=$?

# --- Test Case 2: No git repo, some N/A values ---
echo "--- Setting up Test Case 2: No git repo, some N/A values ---"
create_mock "uptime" "" # Simulate uptime failing
create_mock "hostname" "" # Simulate hostname -I failing
create_mock "df" "" # Simulate df failing
create_mock "free" "" # Simulate free failing
create_mock "pwd" "/tmp/test_area"
# No git mock, so it should fall through to "Not a Git repository"
rm -f "$TEST_DIR/git" # Ensure git mock is removed for this test

EXPECTED_OUTPUT_2="$TEST_DIR/expected_output_2.txt"
ACTUAL_OUTPUT_2="$TEST_DIR/actual_output_2.txt"

cat <<EOF > "$EXPECTED_OUTPUT_2"

\033[0;36m--- Nightly Digital Nomad's Compass ---\033[0m
\033[0;32mUptime:\033[0m N/A
\033[0;33mIP Address:\033[0m N/A
\033[0;34mDisk Usage:\033[0m N/A
\033[0;35mMemory Usage:\033[0m N/A
\033[0;36mCurrent Path:\033[0m /tmp/test_area
\033[0;32mGit Status:\033[0m Not a Git repository
\033[0;36m---------------------------------------\033[0m

EOF

run_test "No git repo, some N/A values" "$EXPECTED_OUTPUT_2" "$ACTUAL_OUTPUT_2"
TEST_RESULT_2=$?

# --- Test Case 3: Git repo with uncommitted changes ---
echo "--- Setting up Test Case 3: Git repo with uncommitted changes ---"
create_mock "uptime" "up 2 days, 1 hour"
create_mock "hostname" "10.0.0.5"
create_mock "df" "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sdb1       200G  150G   50G  75% /data"
create_mock "free" "              total        used        free      shared  buff/cache   available\nMem:           31Gi       16Gi       10Gi       2.0Gi       5.0Gi        15Gi"
create_mock "pwd" "/home/user/another_project"
create_git_mock "## feature/branch\nM  file1.txt\n?? new_file.txt\n" # git status --short --branch output for dirty repo

EXPECTED_OUTPUT_3="$TEST_DIR/expected_output_3.txt"
ACTUAL_OUTPUT_3="$TEST_DIR/actual_output_3.txt"

cat <<EOF > "$EXPECTED_OUTPUT_3"

\033[0;36m--- Nightly Digital Nomad's Compass ---\033[0m
\033[0;32mUptime:\033[0m up 2 days, 1 hour
\033[0;33mIP Address:\033[0m 10.0.0.5
\033[0;34mDisk Usage:\033[0m 75% used of 200G
\033[0;35mMemory Usage:\033[0m 16Gi used of 31Gi
\033[0;36mCurrent Path:\033[0m /home/user/another_project
\033[0;32mGit Status:\033[0m
  ## feature/branch
  M  file1.txt
  ?? new_file.txt
\033[0;36m---------------------------------------\033[0m

EOF

run_test "Git repo with uncommitted changes" "$EXPECTED_OUTPUT_3" "$ACTUAL_OUTPUT_3"
TEST_RESULT_3=$?

# --- Final Result ---
if [[ $TEST_RESULT_1 -eq 0 && $TEST_RESULT_2 -eq 0 && $TEST_RESULT_3 -eq 0 ]]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
