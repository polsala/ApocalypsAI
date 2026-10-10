#!/bin/bash

# Mock rationale: We need to simulate a git repository's file history
# without actually creating one or relying on the host's git.
# This mock provides predictable outputs for 'git ls-files' and 'git log'.

# --- MOCK GIT COMMANDS ---
MOCKED_FILES=(
    "ancient_doc.md"
    "recent_code.py"
    "stale_script.sh"
    "new_feature.js"
    "another_ancient.txt"
)

# Associative array for mocked git log timestamps (file -> timestamp)
declare -A MOCKED_TIMESTAMPS
# Current time for reference (e.g., 2024-01-01 00:00:00 UTC)
MOCK_CURRENT_TIMESTAMP=1704067200 # Jan 1, 2024 00:00:00 UTC

# Define relative ages for files
# ancient_doc.md: 400 days old (stale for 365-day threshold)
MOCKED_TIMESTAMPS["ancient_doc.md"]=$((MOCK_CURRENT_TIMESTAMP - (400 * 24 * 60 * 60)))
# recent_code.py: 100 days old (not stale)
MOCKED_TIMESTAMPS["recent_code.py"]=$((MOCK_CURRENT_TIMESTAMP - (100 * 24 * 60 * 60)))
# stale_script.sh: 500 days old (stale)
MOCKED_TIMESTAMPS["stale_script.sh"]=$((MOCK_CURRENT_TIMESTAMP - (500 * 24 * 60 * 60)))
# new_feature.js: 10 days old (not stale)
MOCKED_TIMESTAMPS["new_feature.js"]=$((MOCK_CURRENT_TIMESTAMP - (10 * 24 * 60 * 60)))
# another_ancient.txt: 700 days old (stale)
MOCKED_TIMESTAMPS["another_ancient.txt"]=$((MOCK_CURRENT_TIMESTAMP - (700 * 24 * 60 * 60)))

git() {
    local cmd=$1
    shift
    if [ "$cmd" == "ls-files" ]; then
        for file in "${MOCKED_FILES[@]}"; do
            echo "$file"
        done
    elif [ "$cmd" == "log" ]; then
        local format=""
        local file=""
        while [[ $# -gt 0 ]]; do
            key="$1"
            case $key in
                -1) ;;
                --format=*)
                    format="${key#--format=}"
                    ;;
                --)
                    shift
                    file="$1"
                    ;;
                *)
                    file="$key"
                    ;;
            esac
            shift
        done

        if [ "$format" == "%at" ] && [ -n "$file" ]; then
            if [[ -v MOCKED_TIMESTAMPS["$file"] ]]; then
                echo "${MOCKED_TIMESTAMPS["$file"]}"
            else
                # File not in mock, simulate no history
                return 1
            fi
        else
            echo "Mocked git log received unexpected arguments: $@" >&2
            return 1
        fi
    else
        echo "Mocked git received unexpected command: $cmd" >&2
        return 1
    fi
}

# Mock rationale: We need to control the "current time" for age calculations
# to ensure deterministic test results regardless of when the test is run.
date() {
    if [ "$1" == "+%s" ]; then
        echo "$MOCK_CURRENT_TIMESTAMP"
    else
        /bin/date "$@" # Fallback to real date for other formats if needed, though not for this test.
    fi
}
# --- END MOCK GIT COMMANDS ---

# Source the script to be tested
SCRIPT_TO_TEST_PATH="./src/check_stale_files.sh"

# Test Case 1: Default threshold (365 days)
echo "--- Test Case 1: Default threshold (365 days) ---"
EXPECTED_STALE_DEFAULT=$(echo -e "ancient_doc.md\nstale_script.sh\nanother_ancient.txt")
ACTUAL_STALE_DEFAULT=$(bash "$SCRIPT_TO_TEST_PATH" 365)

if [ "$ACTUAL_STALE_DEFAULT" == "$EXPECTED_STALE_DEFAULT" ]; then
    echo "PASS: Default threshold identified correct stale files."
else
    echo "FAIL: Default threshold."
    echo "Expected:\n$EXPECTED_STALE_DEFAULT"
    echo "Actual:\n$ACTUAL_STALE_DEFAULT"
    exit 1
fi

# Test Case 2: Shorter threshold (150 days) - more files should be stale
echo "--- Test Case 2: Shorter threshold (150 days) ---"
EXPECTED_STALE_SHORT=$(echo -e "ancient_doc.md\nrecent_code.py\nstale_script.sh\nanother_ancient.txt")
ACTUAL_STALE_SHORT=$(bash "$SCRIPT_TO_TEST_PATH" 150)

if [ "$ACTUAL_STALE_SHORT" == "$EXPECTED_STALE_SHORT" ]; then
    echo "PASS: Shorter threshold identified correct stale files."
else
    echo "FAIL: Shorter threshold."
    echo "Expected:\n$EXPECTED_STALE_SHORT"
    echo "Actual:\n$ACTUAL_STALE_SHORT"
    exit 1
fi

# Test Case 3: Very long threshold (1000 days) - no files should be stale
echo "--- Test Case 3: Very long threshold (1000 days) ---"
EXPECTED_STALE_LONG=""
ACTUAL_STALE_LONG=$(bash "$SCRIPT_TO_TEST_PATH" 1000)

if [ "$ACTUAL_STALE_LONG" == "$EXPECTED_STALE_LONG" ]; then
    echo "PASS: Long threshold identified no stale files."
else
    echo "FAIL: Long threshold."
    echo "Expected:\n'$EXPECTED_STALE_LONG'"
    echo "Actual:\n'$ACTUAL_STALE_LONG'"
    exit 1
fi

echo "All tests passed!"
exit 0
