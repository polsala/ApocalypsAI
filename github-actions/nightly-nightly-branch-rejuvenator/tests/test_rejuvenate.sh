#!/bin/bash
set -euo pipefail

# Mock rationale: Simulates git commands to control branch history and push operations
# without actual git repository interactions or network calls.
# This allows deterministic testing of the rejuvenation logic.

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
cd "${TEST_DIR}"

# Store actual git path
REAL_GIT=$(which git | grep -v "${TEST_DIR}/bin" || true) # '|| true' to prevent error if git not found in PATH

# Create a dummy git repository using the real git
"${REAL_GIT}" init -b main > /dev/null 2>&1
echo "initial commit" > file.txt
"${REAL_GIT}" add file.txt
"${REAL_GIT}" commit -m "Initial commit" > /dev/null 2>&1

# Create a mock 'git' executable
mkdir -p "${TEST_DIR}/bin"
export PATH="${TEST_DIR}/bin:${PATH}"

# Mock git log to return specific timestamps
# Mock git checkout to do nothing
# Mock git commit to do nothing
# Mock git push to record pushes
cat << 'EOF' > "${TEST_DIR}/bin/git"
#!/bin/bash

# Use the real git for commands not explicitly mocked
REAL_GIT_PATH="${REAL_GIT}"

if [[ "$1" == "log" && "$2" == "-1" && "$3" == "--format=%at" ]]; then
    branch_ref="$4"
    case "$branch_ref" in
        "origin/feature/stale-branch")
            # 60 days ago
            echo $(( $(date +%s) - (60 * 24 * 60 * 60) ))
            ;;
        "origin/feature/active-branch")
            # 5 days ago
            echo $(( $(date +%s) - (5 * 24 * 60 * 60) ))
            ;;
        "origin/feature/excluded-branch")
            # 60 days ago, but should be excluded
            echo $(( $(date +%s) - (60 * 24 * 60 * 60) ))
            ;;
        "origin/main")
            # Main branch, should be excluded by default
            echo $(( $(date +%s) - (10 * 24 * 60 * 60) ))
            ;;
        *)
            # Fallback for other branches or actual git commands
            "${REAL_GIT_PATH}" "$@"
            ;;
    esac
elif [[ "$1" == "branch" && "$2" == "-r" ]]; then
    echo "  origin/HEAD -> origin/main"
    echo "  origin/main"
    echo "  origin/feature/stale-branch"
    echo "  origin/feature/active-branch"
    echo "  origin/feature/excluded-branch"
elif [[ "$1" == "checkout" ]]; then
    echo "MOCK: git checkout $2"
elif [[ "$1" == "commit" ]]; then
    echo "MOCK: git commit $@"
elif [[ "$1" == "push" ]]; then
    echo "MOCK: git push $@"
    echo "$3" >> "${TEST_DIR}/pushed_branches.log" # Record the branch that was "pushed"
elif [[ "$1" == "remote" ]]; then
    echo "MOCK: git remote $@"
elif [[ "$1" == "fetch" ]]; then
    echo "MOCK: git fetch $@"
elif [[ "$1" == "config" ]]; then
    echo "MOCK: git config $@"
else
    # For other git commands like init, add, commit in setup
    "${REAL_GIT_PATH}" "$@"
fi
EOF
chmod +x "${TEST_DIR}/bin/git"

# Create mock jq
cat << 'EOF' > "${TEST_DIR}/bin/jq"
#!/bin/bash
# Simple mock for jq -R . | jq -s . to just wrap lines in JSON array
# This is sufficient for testing the output format for a single or zero rejuvenated branch.
readarray -t lines
printf '['
first=true
for line in "${lines[@]}"; do
    if ! $first; then
        printf ','
    fi
    printf '"%s"' "$line"
    first=false
done
printf ']\n'
EOF
chmod +x "${TEST_DIR}/bin/jq"

# Create mock shuf
cat << 'EOF' > "${TEST_DIR}/bin/shuf"
#!/bin/bash
# Mock shuf to return a deterministic message for testing
echo "You've been missed! Time to shine again."
EOF
chmod +x "${TEST_DIR}/bin/shuf"

# --- Test Execution ---
echo "Running rejuvenation script..."

# Simulate GitHub Actions environment variables
export INPUT_DAYS_STALE="30"
export INPUT_COMMIT_MESSAGE_PREFIX="Test Rejuvenation:"
export INPUT_EXCLUDE_BRANCHES="main,master,feature/excluded-branch"
export INPUT_GITHUB_TOKEN="ghs_mocktoken" # Mock token
export GITHUB_REPOSITORY="test/repo"
export GITHUB_OUTPUT="${TEST_DIR}/github_output.txt" # Redirect GITHUB_OUTPUT

# Source the script to be tested
# Copy the script to the test directory to simulate github.action_path
cp ../src/rejuvenate.sh .
./rejuvenate.sh

# --- Assertions ---
echo "Verifying results..."

# Check which branches were "pushed"
if [[ -f "${TEST_DIR}/pushed_branches.log" ]]; then
    PUSHED_BRANCHES=$(cat "${TEST_DIR}/pushed_branches.log")
else
    PUSHED_BRANCHES=""
fi

EXPECTED_PUSHED_BRANCH="feature/stale-branch"

if [[ "${PUSHED_BRANCHES}" == "${EXPECTED_PUSHED_BRANCH}" ]]; then
    echo "Test PASSED: Correct branch '${EXPECTED_PUSHED_BRANCH}' was rejuvenated."
else
    echo "Test FAILED: Expected '${EXPECTED_PUSHED_BRANCH}' to be rejuvenated, but got '${PUSHED_BRANCHES}'."
    exit 1
fi

# Check GITHUB_OUTPUT
if [[ -f "${GITHUB_OUTPUT}" ]]; then
    OUTPUT_CONTENT=$(cat "${GITHUB_OUTPUT}")
    EXPECTED_OUTPUT_SUBSTRING="rejuvenated-branches=[\"feature/stale-branch\"]"
    if [[ "${OUTPUT_CONTENT}" == *"${EXPECTED_OUTPUT_SUBSTRING}"* ]]; then
        echo "Test PASSED: GITHUB_OUTPUT contains expected rejuvenated branches."
    else
        echo "Test FAILED: GITHUB_OUTPUT did not contain expected value."
        echo "Expected substring: '${EXPECTED_OUTPUT_SUBSTRING}'"
        echo "Actual output: '${OUTPUT_CONTENT}'"
        exit 1
    fi
else
    echo "Test FAILED: GITHUB_OUTPUT file not created."
    exit 1
fi

echo "All tests passed!"

# --- Cleanup ---
rm -rf "${TEST_DIR}"
