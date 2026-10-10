#!/bin/bash

# Test script for graveyard_keeper.sh

# --- Setup Mock Git Environment ---
# Mock rationale: We cannot rely on a real git repository for deterministic, offline tests.
# We will create a temporary directory, initialize a git repo, and simulate branches
# with specific commit dates. We'll also mock the `git` command itself to control its output.

TEMP_DIR=$(mktemp -d)
ORIGINAL_PATH=$PATH
export PATH="$TEMP_DIR:$PATH" # Prepend TEMP_DIR to PATH so our mock git is found first

# Create a mock git executable
cat << 'EOF' > "$TEMP_DIR/git"
#!/bin/bash
# This is a mock git command for testing graveyard_keeper.sh

# Mock git branch -r output
if [[ "$1" == "branch" && "$2" == "-r" ]]; then
    echo "  origin/main"
    echo "  origin/feature-new"
    echo "  origin/feature-old"
    echo "  origin/feature-ancient"
    echo "  origin/release/v1.0"
    echo "  origin/bugfix/critical"
    echo "  origin/ignored-branch"
    exit 0
fi

# Mock git log -1 --format="%ct" output
if [[ "$1" == "log" && "$2" == "-1" && "$3" == "--format=%ct" ]]; then
    case "$4" in
        "origin/main")
            echo "$(date -d '1 day ago' +%s)" # Recent
            ;;
        "origin/feature-new")
            echo "$(date -d '5 days ago' +%s)" # Recent
            ;;
        "origin/feature-old")
            echo "$(date -d '100 days ago' +%s)" # Stale (if threshold is 90)
            ;;
        "origin/feature-ancient")
            echo "$(date -d '200 days ago' +%s)" # Very Stale
            ;;
        "origin/release/v1.0")
            echo "$(date -d '30 days ago' +%s)" # Recent
            ;;
        "origin/bugfix/critical")
            echo "$(date -d '60 days ago' +%s)" # Recent
            ;;
        "origin/ignored-branch")
            echo "$(date -d '300 days ago' +%s)" # Stale, but ignored
            ;;
        *)
            echo "0" # Default for unknown branches, should not happen with our mock list
            ;;
    esac
    exit 0
fi

# Fallback for any other git commands (shouldn't be called by graveyard_keeper.sh)
echo "Mock git: Unknown command: $@" >&2
exit 1
EOF
chmod +x "$TEMP_DIR/git"

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local stale_days="$2"
    local ignore_branches="$3"
    local expected_output_json="$4"

    echo "Running test: $test_name"
    # Execute the script with mocked git
    ACTUAL_OUTPUT=$(bash ../src/graveyard_keeper.sh "$stale_days" "$ignore_branches")

    if [ "$ACTUAL_OUTPUT" == "$expected_output_json" ]; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "  Expected: $expected_output_json"
        echo "  Actual:   $ACTUAL_OUTPUT"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: Default stale days (90), default ignore branches (main,master,develop)
# Expected: feature-old (100 days), feature-ancient (200 days)
run_test "Default parameters" "90" "main,master,develop" "[\"feature-old\",\"feature-ancient\"]"

# Test 2: Shorter stale days (30), default ignore branches
# Expected: bugfix/critical (60), feature-old (100), feature-ancient (200)
run_test "Shorter stale days (30)" "30" "main,master,develop" "[\"bugfix/critical\",\"feature-old\",\"feature-ancient\"]"

# Test 3: Longer stale days (150), default ignore branches
# Expected: feature-ancient (200)
run_test "Longer stale days (150)" "150" "main,master,develop" "[\"feature-ancient\"]"

# Test 4: Custom ignore branches (including 'feature-old' and 'ignored-branch')
# Expected: feature-ancient (200)
run_test "Custom ignore branches" "90" "main,master,develop,feature-old,ignored-branch" "[\"feature-ancient\"]"

# Test 5: No ignore branches
# Expected: feature-old (100), feature-ancient (200), ignored-branch (300)
run_test "No ignore branches" "90" "" "[\"feature-old\",\"feature-ancient\",\"ignored-branch\"]"

# Test 6: All branches ignored (regex pattern)
# Expected: []
run_test "All branches ignored (regex)" "90" ".*" "[]"

# Test 7: No stale branches (very high stale days)
# Expected: []
run_test "No stale branches" "500" "main,master,develop" "[]"

# --- Cleanup ---
rm -rf "$TEMP_DIR"
export PATH="$ORIGINAL_PATH" # Restore original PATH

echo "All tests passed!"
