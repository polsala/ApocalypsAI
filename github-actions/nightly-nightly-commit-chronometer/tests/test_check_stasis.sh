#!/bin/bash

# Mock rationale: We need to control the output of 'git log' and 'date' for deterministic testing.
# We cannot rely on the actual git history or current system time, which would make tests non-deterministic.

# --- Test Setup ---
# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR" || exit 1

# Create a mock bin directory and prepend it to PATH
mkdir -p "$TEST_DIR/mock_bin"
export PATH="$TEST_DIR/mock_bin:$PATH"

# Create mock git executable
cat << 'EOF' > "$TEST_DIR/mock_bin/git"
#!/bin/bash
if [[ "$1" == "log" && "$2" == "-1" && "$3" == "--format=%cd" && "$4" == "--date=iso-strict" ]]; then
  echo "$MOCKED_GIT_LOG_OUTPUT"
else
  echo "Error: Unexpected git command: $*" >&2
  exit 1
fi
EOF
chmod +x "$TEST_DIR/mock_bin/git"

# Create mock date executable
cat << 'EOF' > "$TEST_DIR/mock_bin/date"
#!/bin/bash
if [[ "$1" == "-d" && "$3" == "+%s" ]]; then
  case "$2" in
    "2023-01-01T00:00:00+00:00") echo "$MOCKED_DATE_TIMESTAMP_OLD" ;;
    "2023-01-08T00:00:00+00:00") echo "$MOCKED_DATE_TIMESTAMP_RECENT" ;;
    *) echo "Error: Unexpected date string for timestamp conversion: $2" >&2; exit 1 ;;
  esac
elif [[ "$1" == "+%s" ]]; then
  echo "$MOCKED_CURRENT_TIMESTAMP"
else
  echo "Error: Unexpected date command: $*" >&2
  exit 1
fi
EOF
chmod +x "$TEST_DIR/mock_bin/date"

# Path to the script to be tested (relative to the test script itself)
SCRIPT_TO_TEST="$(dirname "$0")"/../src/check_stasis.sh

# --- Test Cases ---

# Test 1: No stasis detected (commit is recent)
echo "--- Running Test 1: No stasis detected ---"
export MOCKED_GIT_LOG_OUTPUT="2023-01-08T00:00:00+00:00" # Last commit is Jan 8
export MOCKED_DATE_TIMESTAMP_OLD="1672531200" # Jan 1, 2023 00:00:00 UTC
export MOCKED_DATE_TIMESTAMP_RECENT="1673136000" # Jan 8, 2023 00:00:00 UTC
export MOCKED_CURRENT_TIMESTAMP="1673136000" # Current time is Jan 8 (0 days old)
GITHUB_OUTPUT=$(mktemp) # Temporary file to capture GITHUB_OUTPUT
export GITHUB_OUTPUT

# Run the script with max-stasis-days=7, fail-on-stasis=false
bash "$SCRIPT_TO_TEST" "7" "false"
EXIT_CODE=$?

if [ "$EXIT_CODE" -ne 0 ]; then
  echo "Test 1 FAILED: Script exited with code $EXIT_CODE"
  cat "$GITHUB_OUTPUT"
  exit 1
fi

OUTPUT_CONTENT=$(cat "$GITHUB_OUTPUT")
if ! echo "$OUTPUT_CONTENT" | grep -q "stasis-detected=false"; then
  echo "Test 1 FAILED: Expected stasis-detected=false, got:"
  cat "$GITHUB_OUTPUT"
  exit 1
fi
if ! echo "$OUTPUT_CONTENT" | grep -q "commit-age-days=0"; then
  echo "Test 1 FAILED: Expected commit-age-days=0, got:"
  cat "$GITHUB_OUTPUT"
  exit 1
fi
echo "Test 1 PASSED."

# Test 2: Stasis detected, warning only (commit is old, fail-on-stasis=false)
echo "--- Running Test 2: Stasis detected, warning only ---"
export MOCKED_GIT_LOG_OUTPUT="2023-01-01T00:00:00+00:00" # Last commit is Jan 1
export MOCKED_DATE_TIMESTAMP_OLD="1672531200" # Jan 1, 2023 00:00:00 UTC
export MOCKED_DATE_TIMESTAMP_RECENT="1673136000" # Jan 8, 2023 00:00:00 UTC (not used here, but for consistency)
export MOCKED_CURRENT_TIMESTAMP="1673136000" # Current time is Jan 8 (7 days old)
GITHUB_OUTPUT=$(mktemp) # Reset GITHUB_OUTPUT
export GITHUB_OUTPUT

# Run the script with max-stasis-days=6, fail-on-stasis=false
bash "$SCRIPT_TO_TEST" "6" "false"
EXIT_CODE=$?

if [ "$EXIT_CODE" -ne 0 ]; then
  echo "Test 2 FAILED: Script exited with code $EXIT_CODE"
  cat "$GITHUB_OUTPUT"
  exit 1
fi

OUTPUT_CONTENT=$(cat "$GITHUB_OUTPUT")
if ! echo "$OUTPUT_CONTENT" | grep -q "stasis-detected=true"; then
  echo "Test 2 FAILED: Expected stasis-detected=true, got:"
  cat "$GITHUB_OUTPUT"
  exit 1
fi
if ! echo "$OUTPUT_CONTENT" | grep -q "commit-age-days=7"; then
  echo "Test 2 FAILED: Expected commit-age-days=7, got:"
  cat "$GITHUB_OUTPUT"
  exit 1
fi
echo "Test 2 PASSED."

# Test 3: Stasis detected, failure (commit is old, fail-on-stasis=true)
echo "--- Running Test 3: Stasis detected, failure ---"
export MOCKED_GIT_LOG_OUTPUT="2023-01-01T00:00:00+00:00" # Last commit is Jan 1
export MOCKED_DATE_TIMESTAMP_OLD="1672531200" # Jan 1, 2023 00:00:00 UTC
export MOCKED_DATE_TIMESTAMP_RECENT="1673136000" # Jan 8, 2023 00:00:00 UTC (not used here)
export MOCKED_CURRENT_TIMESTAMP="1673136000" # Current time is Jan 8 (7 days old)
GITHUB_OUTPUT=$(mktemp) # Reset GITHUB_OUTPUT
export GITHUB_OUTPUT

# Run the script with max-stasis-days=6, fail-on-stasis=true
bash "$SCRIPT_TO_TEST" "6" "true"
EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "Test 3 FAILED: Script was expected to fail, but exited with code $EXIT_CODE"
  cat "$GITHUB_OUTPUT"
  exit 1
fi

echo "Test 3 PASSED (script failed as expected)."

# --- Cleanup ---
rm -rf "$TEST_DIR"
echo "All tests completed."
