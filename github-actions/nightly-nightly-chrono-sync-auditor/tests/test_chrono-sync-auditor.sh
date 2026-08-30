#!/bin/bash
set -euo pipefail

# Mock rationale: This test creates a temporary Git repository and manipulates file timestamps
# directly using standard system commands (git, touch, stat). It does not rely on external
# services or network calls, making it deterministic and offline.

echo "Running Chrono-Sync Auditor tests..."

# Create a temporary directory for the test repository
TEST_REPO_DIR=$(mktemp -d)
cd "$TEST_REPO_DIR"

# Mock GITHUB_OUTPUT for testing
MOCKED_GITHUB_OUTPUT=$(mktemp)
export GITHUB_OUTPUT="$MOCKED_GITHUB_OUTPUT"

# Simulate the action's composite step logic in a function
run_action_logic() {
    local fail_on_anomaly="${1:-true}"
    
    ANOMALIES=""
    ANOMALIES_COUNT=0
    
    # Ensure git is available
    if ! command -v git &> /dev/null; then
        echo "Error: git command not found. Please ensure git is installed in the runner environment."
        exit 1
    fi

    # Ensure stat is available and supports %Y
    if ! stat -c %Y . &> /dev/null; then
        echo "Error: stat command does not support %Y. Please ensure a GNU-compatible stat is available."
        exit 1
    fi

    git ls-files -z | while IFS= read -r -d $'\0' file; do
        if [ -f "$file" ]; then
            LAST_COMMIT_TIME=$(git log -1 --format="%ct" -- "$file" 2>/dev/null)
            if [ -z "$LAST_COMMIT_TIME" ]; then
                continue
            fi
            
            FILE_MTIME=$(stat -c %Y "$file")

            if [ "$FILE_MTIME" -lt "$LAST_COMMIT_TIME" ]; then
                echo "🚨 Anomaly detected: '$file' (mtime: $(date -d @$FILE_MTIME +'%Y-%m-%d %H:%M:%S') < last commit: $(date -d @$LAST_COMMIT_TIME +'%Y-%m-%d %H:%M:%S'))"
                ANOMALIES="${ANOMALIES}${file}\n"
                ANOMALIES_COUNT=$((ANOMALIES_COUNT + 1))
            fi
        fi
    done

    if [ "$ANOMALIES_COUNT" -gt 0 ]; then
        echo "::warning::Found $ANOMALIES_COUNT chronological anomalies."
        echo "anomalies-found=true" >> "$GITHUB_OUTPUT"
        echo "anomaly-list<<EOF" >> "$GITHUB_OUTPUT"
        echo -e "$ANOMALIES" >> "$GITHUB_OUTPUT"
        echo "EOF" >> "$GITHUB_OUTPUT"
        if [[ "$fail_on_anomaly" == "true" ]]; then
            echo "::error::Failing due to chronological anomalies."
            return 1 # Indicate failure
        fi
    else
        echo "✅ No chronological anomalies detected. All files are in sync with their last commit times."
        echo "anomalies-found=false" >> "$GITHUB_OUTPUT"
        echo "anomaly-list=" >> "$GITHUB_OUTPUT"
    fi
    return 0 # Indicate success
}

# --- Test Case 1: No anomalies (freshly committed files) ---
echo "--- Test Case 1: No anomalies (freshly committed files) ---"
git init -b main > /dev/null
echo "Hello World" > file1.txt
git add file1.txt
git commit -m "Initial commit file1" > /dev/null
sleep 1 # Ensure distinct timestamps
echo "Another file" > file2.txt
git add file2.txt
git commit -m "Add file2" > /dev/null

# Run with fail-on-anomaly=true (default)
if ! run_action_logic "true"; then
    echo "Test Case 1 FAILED: Action unexpectedly failed."
    exit 1
fi

# Assert outputs
if ! grep -q "anomalies-found=false" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 1 FAILED: Expected 'anomalies-found=false', but got different."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi
if grep -q "anomaly-list=" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 1 PASSED: No anomalies detected as expected."
else
    echo "Test Case 1 FAILED: Expected 'anomaly-list=' to be empty, but it was not."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi

# Clear GITHUB_OUTPUT for next test
> "$MOCKED_GITHUB_OUTPUT"

# --- Test Case 2: Anomaly detected ---
echo "--- Test Case 2: Anomaly detected (file mtime older than commit) ---"
# Create a new file, commit it
echo "New content" > file3.txt
git add file3.txt
git commit -m "Add file3" > /dev/null

# Get the commit time for file3.txt
FILE3_COMMIT_TIME=$(git log -1 --format="%ct" -- file3.txt)

# Set file3.txt's modification time to be older than its commit time
# Subtract 100 seconds from commit time
OLD_MTIME=$((FILE3_COMMIT_TIME - 100))
touch -d "@$OLD_MTIME" file3.txt

# Run with fail-on-anomaly=true (default)
if run_action_logic "true"; then
    echo "Test Case 2 FAILED: Action unexpectedly succeeded."
    exit 1
fi

# Assert outputs
if ! grep -q "anomalies-found=true" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 2 FAILED: Expected 'anomalies-found=true', but got different."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi
if ! grep -q "file3.txt" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 2 FAILED: Expected 'file3.txt' in anomaly list, but it was not."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi
echo "Test Case 2 PASSED: Anomaly detected as expected."

# Clear GITHUB_OUTPUT for next test
> "$MOCKED_GITHUB_OUTPUT"

# --- Test Case 3: Anomaly detected, but fail-on-anomaly is false ---
echo "--- Test Case 3: Anomaly detected, but fail-on-anomaly is false ---"
# Re-use file3.txt with its old mtime
# Run with fail-on-anomaly=false
if ! run_action_logic "false"; then
    echo "Test Case 3 FAILED: Action unexpectedly failed with fail-on-anomaly=false."
    exit 1
fi

# Assert outputs
if ! grep -q "anomalies-found=true" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 3 FAILED: Expected 'anomalies-found=true', but got different."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi
if ! grep -q "file3.txt" "$MOCKED_GITHUB_OUTPUT"; then
    echo "Test Case 3 FAILED: Expected 'file3.txt' in anomaly list, but it was not."
    cat "$MOCKED_GITHUB_OUTPUT"
    exit 1
fi
echo "Test Case 3 PASSED: Anomaly detected but action did not fail."

# Cleanup
rm -rf "$TEST_REPO_DIR"
rm "$MOCKED_GITHUB_OUTPUT"

echo "All Chrono-Sync Auditor tests passed!"
