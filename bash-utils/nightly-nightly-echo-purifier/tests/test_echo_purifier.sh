#!/bin/bash

# Automated tests for nightly-echo-purifier

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# Define the path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/echo_purifier.sh

# --- Test Setup ---

# Create a temporary directory for test files
TEST_DIR=$(mktemp -d)

# Function to clean up the temporary directory
cleanup() {
    rm -rf "$TEST_DIR"
}

# Register the cleanup function to be called on script exit
trap cleanup EXIT

# Create test directories
DIR1="$TEST_DIR/dir1"
DIR2="$TEST_DIR/dir2"
mkdir -p "$DIR1" "$DIR2"

# --- Mocking md5sum ---

# Mock rationale: md5sum is an external command. Mocking it ensures tests are deterministic and don't rely on actual file content hashing,
# which could vary across systems or be slow. It also allows testing specific duplicate scenarios without creating large files.

# Override md5sum function for testing purposes
md5sum() {
    local file_path="$1"
    local file_name=$(basename "$file_path")
    case "$file_name" in
        "unique_file_A.txt") echo "mock_checksum_A  $file_path" ;;
        "unique_file_B.txt") echo "mock_checksum_B  $file_path" ;;
        "duplicate_file_C.txt") echo "mock_checksum_C  $file_path" ;;
        "duplicate_file_C_copy.txt") echo "mock_checksum_C  $file_path" ;;
        "duplicate_file_D.txt") echo "mock_checksum_D  $file_path" ;;
        "duplicate_file_D_another.txt") echo "mock_checksum_D  $file_path" ;;
        "nested_duplicate_E.txt") echo "mock_checksum_E  $file_path" ;;
        "nested_duplicate_E_copy.txt") echo "mock_checksum_E  $file_path" ;;
        *) echo "mock_checksum_UNKNOWN  $file_path" ;;
    esac
}

# --- Test Cases ---

# Test 1: No duplicates
echo "Running Test 1: No duplicates..." >&2

# Create unique files
echo "content A" > "$DIR1/unique_file_A.txt"
echo "content B" > "$DIR2/unique_file_B.txt"

OUTPUT=$(bash "$SCRIPT_PATH" "$DIR1" "$DIR2" 2>&1)

if echo "$OUTPUT" | grep -q "Duplicate Group"; then
    echo "Test 1 FAILED: Detected duplicates when none expected." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
echo "Test 1 PASSED: No duplicates correctly reported." >&2

# Test 2: Duplicates across different directories
echo "Running Test 2: Duplicates across different directories..." >&2

# Create duplicate files
echo "content C" > "$DIR1/duplicate_file_C.txt"
echo "content C" > "$DIR2/duplicate_file_C_copy.txt"

OUTPUT=$(bash "$SCRIPT_PATH" "$DIR1" "$DIR2" 2>&1)

if ! echo "$OUTPUT" | grep -q "Duplicate Group (Checksum: mock_checksum_C):"; then
    echo "Test 2 FAILED: Did not detect expected duplicate group C." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $DIR1/duplicate_file_C.txt"; then
    echo "Test 2 FAILED: Missing file $DIR1/duplicate_file_C.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $DIR2/duplicate_file_C_copy.txt"; then
    echo "Test 2 FAILED: Missing file $DIR2/duplicate_file_C_copy.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
echo "Test 2 PASSED: Duplicates across directories correctly reported." >&2

# Test 3: Duplicates within the same directory
echo "Running Test 3: Duplicates within the same directory..." >&2

# Create duplicate files in DIR1
echo "content D" > "$DIR1/duplicate_file_D.txt"
echo "content D" > "$DIR1/duplicate_file_D_another.txt"

OUTPUT=$(bash "$SCRIPT_PATH" "$DIR1" 2>&1)

if ! echo "$OUTPUT" | grep -q "Duplicate Group (Checksum: mock_checksum_D):"; then
    echo "Test 3 FAILED: Did not detect expected duplicate group D." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $DIR1/duplicate_file_D.txt"; then
    echo "Test 3 FAILED: Missing file $DIR1/duplicate_file_D.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $DIR1/duplicate_file_D_another.txt"; then
    echo "Test 3 FAILED: Missing file $DIR1/duplicate_file_D_another.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
echo "Test 3 PASSED: Duplicates within same directory correctly reported." >&2

# Test 4: Nested directories and duplicates
echo "Running Test 4: Nested directories and duplicates..." >&2

NESTED_DIR="$DIR1/nested"
mkdir -p "$NESTED_DIR"
echo "content E" > "$NESTED_DIR/nested_duplicate_E.txt"
echo "content E" > "$DIR1/nested_duplicate_E_copy.txt"

OUTPUT=$(bash "$SCRIPT_PATH" "$DIR1" 2>&1)

if ! echo "$OUTPUT" | grep -q "Duplicate Group (Checksum: mock_checksum_E):"; then
    echo "Test 4 FAILED: Did not detect expected nested duplicate group E." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $NESTED_DIR/nested_duplicate_E.txt"; then
    echo "Test 4 FAILED: Missing file $NESTED_DIR/nested_duplicate_E.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "  - $DIR1/nested_duplicate_E_copy.txt"; then
    echo "Test 4 FAILED: Missing file $DIR1/nested_duplicate_E_copy.txt in output." >&2
    echo "Output:" "$OUTPUT" >&2
    exit 1
fi
echo "Test 4 PASSED: Nested duplicates correctly reported." >&2

# Test 5: No arguments (should show usage and exit with error)
echo "Running Test 5: No arguments..." >&2

if bash "$SCRIPT_PATH" 2>&1 | grep -q "Usage:"; then
    echo "Test 5 PASSED: Usage message displayed for no arguments." >&2
else
    echo "Test 5 FAILED: Usage message not displayed for no arguments." >&2
    exit 1
fi

# Test 6: Non-existent directory (should report error and exit)
echo "Running Test 6: Non-existent directory..." >&2

if bash "$SCRIPT_PATH" "$TEST_DIR/non_existent_dir" 2>&1 | grep -q "Error: Directory '$TEST_DIR/non_existent_dir' not found"; then
    echo "Test 6 PASSED: Error reported for non-existent directory." >&2
else
    echo "Test 6 FAILED: Error not reported for non-existent directory." >&2
    exit 1
fi

echo "\nAll tests completed successfully!" >&2
