#!/bin/bash

# Mock rationale: We need to test the script's logic (classification, manifest generation) without actually moving/creating files on the host system.
# Mocking `mv` and `mkdir` allows us to capture their calls and verify the script's intended actions.
# `find` is not mocked as its behavior is standard and essential for file iteration.
# The manifest file content is verified by checking the script's stdout, as mocking file writes in bash for complex content is overly complex for this utility.

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t stash_sorter_test_XXXXXX)
SOURCE_TEST_DIR="$TEST_DIR/source"
DEST_TEST_ROOT="$TEST_DIR/destination"

# Create source directory
mkdir -p "$SOURCE_TEST_DIR"

# Create dummy files in source directory
touch "$SOURCE_TEST_DIR/document1.txt"
touch "$SOURCE_TEST_DIR/image1.jpg"
touch "$SOURCE_TEST_DIR/archive1.zip"
touch "$SOURCE_TEST_DIR/script1.sh"
touch "$SOURCE_TEST_DIR/data1.json"
touch "$SOURCE_TEST_DIR/unknown_file.xyz"
touch "$SOURCE_TEST_DIR/another_doc.PDF" # Test case-insensitivity
touch "$SOURCE_TEST_DIR/empty_file" # No extension

# Store original commands
ORIG_MV=$(which mv)
ORIG_MKDIR=$(which mkdir)

# Mock commands
MOCKED_MV_CALLS=()
MOCKED_MKDIR_CALLS=()

mv() {
    MOCKED_MV_CALLS+=("$@")
    # Simulate success
    return 0
}

mkdir() {
    MOCKED_MKDIR_CALLS+=("$@")
    # Simulate success
    return 0
}

# Override PATH to use our mocks
export PATH="$(dirname "$0"):$PATH"

# --- Test Functions ---

assert_contains() {
    local haystack="$1"
    local needle="$2"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' to contain '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    }
}

# --- Run the script ---
# Capture stdout for verification
OUTPUT=$("$SOURCE_TEST_DIR/../src/stash_sorter.sh" "$SOURCE_TEST_DIR" "$DEST_TEST_ROOT")
SCRIPT_EXIT_CODE=$?

# --- Assertions ---

echo "--- Running Tests ---"

# 1. Check script exit code
assert_equals 0 "$SCRIPT_EXIT_CODE" "Script should exit successfully"

# 2. Verify mkdir calls for destination root and categories
echo "Verifying mkdir calls..."
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/unknown"
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/documents"
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/images"
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/archives"
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/scripts"
assert_contains "${MOCKED_MKDIR_CALLS[*]}" "$DEST_TEST_ROOT/data"
echo "  mkdir calls verified."

# 3. Verify mv calls for each file
echo "Verifying mv calls..."
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/document1.txt $DEST_TEST_ROOT/documents/document1.txt"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/image1.jpg $DEST_TEST_ROOT/images/image1.jpg"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/archive1.zip $DEST_TEST_ROOT/archives/archive1.zip"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/script1.sh $DEST_TEST_ROOT/scripts/script1.sh"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/data1.json $DEST_TEST_ROOT/data/data1.json"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/unknown_file.xyz $DEST_TEST_ROOT/unknown/unknown_file.xyz"
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/another_doc.PDF $DEST_TEST_ROOT/documents/another_doc.PDF" # Case-insensitivity
assert_contains "${MOCKED_MV_CALLS[*]}" "$SOURCE_TEST_DIR/empty_file $DEST_TEST_ROOT/unknown/empty_file" # No extension -> unknown
echo "  mv calls verified."

# 4. Verify script output for manifest generation messages
echo "Verifying script output for manifest generation messages..."
assert_contains "$OUTPUT" "Sorting 'document1.txt' into 'documents'..."
assert_contains "$OUTPUT" "Sorting 'image1.jpg' into 'images'..."
assert_contains "$OUTPUT" "Sorting 'archive1.zip' into 'archives'..."
assert_contains "$OUTPUT" "Sorting 'script1.sh' into 'scripts'..."
assert_contains "$OUTPUT" "Sorting 'data1.json' into 'data'..."
assert_contains "$OUTPUT" "Sorting 'unknown_file.xyz' into 'unknown' (extension: .xyz)..."
assert_contains "$OUTPUT" "Sorting 'another_doc.PDF' into 'documents'..."
assert_contains "$OUTPUT" "Sorting 'empty_file' into 'unknown' (extension: .)..." # empty_file has no extension, so it's treated as an empty extension.
assert_contains "$OUTPUT" "Manifest generated at '$DEST_TEST_ROOT/stash_manifest.txt'."
echo "  Manifest generation messages verified."

# 5. Test with no files in source directory
echo "Testing with empty source directory..."
EMPTY_SOURCE_DIR="$TEST_DIR/empty_source"
mkdir -p "$EMPTY_SOURCE_DIR"
EMPTY_DEST_ROOT="$TEST_DIR/empty_destination"
EMPTY_OUTPUT=$("$SOURCE_TEST_DIR/../src/stash_sorter.sh" "$EMPTY_SOURCE_DIR" "$EMPTY_DEST_ROOT")
EMPTY_SCRIPT_EXIT_CODE=$?

assert_equals 0 "$EMPTY_SCRIPT_EXIT_CODE" "Script should exit successfully for empty source"
assert_contains "$EMPTY_OUTPUT" "Starting file sorting from '$EMPTY_SOURCE_DIR'..."
assert_contains "$EMPTY_OUTPUT" "Sorting complete. Manifest generated at '$EMPTY_DEST_ROOT/stash_manifest.txt'."
assert_not_contains "$EMPTY_OUTPUT" "Sorting '" # No files should be sorted
echo "  Empty source directory test passed."

# 6. Test with invalid source directory
echo "Testing with invalid source directory..."
INVALID_SOURCE_DIR="$TEST_DIR/non_existent_dir"
ERROR_OUTPUT=$("$SOURCE_TEST_DIR/../src/stash_sorter.sh" "$INVALID_SOURCE_DIR" 2>&1)
ERROR_SCRIPT_EXIT_CODE=$?

assert_equals 1 "$ERROR_SCRIPT_EXIT_CODE" "Script should exit with error for invalid source"
assert_contains "$ERROR_OUTPUT" "Error: Source directory '$INVALID_SOURCE_DIR' not found."
echo "  Invalid source directory test passed."

# --- Cleanup ---
echo "Cleaning up test directory: $TEST_DIR"
rm -rf "$TEST_DIR"

echo "All tests passed!"
