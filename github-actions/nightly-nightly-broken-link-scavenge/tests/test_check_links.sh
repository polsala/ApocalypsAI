#!/bin/bash

# Nightly Broken Link Scavenger - Test Script

# Mock rationale: To ensure deterministic and offline tests, the 'curl' command
# is mocked. This mock function intercepts network requests and returns
# predefined HTTP status codes based on the URL, avoiding actual network calls.

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/src/check_links.sh

# --- Mocking curl for testing ---
mock_curl_status_code() {
  local url="$1"
  case "$url" in
    "https://good.example.com/page")
      echo "200"
      ;;
    "https://redirect.example.com/old")
      # curl -L would follow, so we simulate the final 200
      echo "200"
      ;;
    "https://broken.example.com/404")
      echo "404"
      ;;
    "http://unavailable.example.com/service")
      echo "500"
      ;;
    "https://timeout.example.com/slow")
      echo "000" # Simulate connection error/timeout
      ;;
    "https://ignored.example.com/path")
      echo "200" # Should be ignored by pattern, but mock returns 200 anyway
      ;;
    "https://another-ignored.example.com")
      echo "403" # Should be ignored by pattern, but mock returns 403 anyway
      ;;
    "https://good-internal.com/doc")
      echo "200"
      ;;
    "https://broken-internal.com/doc")
      echo "404"
      ;;
    *)
      echo "000" # Default for unknown URLs (connection error)
      ;;
  esac
}

# Override the fetch_url_status function from the script with our mock
# This requires the original script to export the function, or we redefine it here.
# For simplicity, we'll redefine it here, assuming the script is sourced or run in a way
# that allows this override.

# Define a mock fetch_url_status that uses our mock_curl_status_code
fetch_url_status() {
  local url="$1"
  # We don't care about HEAD vs GET in the mock, just return the predefined status
  mock_curl_status_code "$url"
}

export -f fetch_url_status # Export the mock function

# --- Test setup ---
TEST_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Create dummy markdown files
mkdir -p "$TEST_DIR/docs"

cat > "$TEST_DIR/README.md" << EOF
# Project Readme

This is a good link: [Good Link](https://good.example.com/page)
This link redirects: [Redirect Link](https://redirect.example.com/old)
This link is broken: [Broken Link](https://broken.example.com/404)

Another broken one: [Unavailable Service](http://unavailable.example.com/service)

An ignored link: [Ignored Link](https://ignored.example.com/path)
Another ignored link: [Another Ignored](https://another-ignored.example.com)

EOF

cat > "$TEST_DIR/docs/guide.md" << EOF
# Guide

Internal good link: [Internal Good](https://good-internal.com/doc)
Internal broken link: [Internal Broken](https://broken-internal.com/doc)

EOF

# --- Test cases ---

echo "Running tests for Nightly Broken Link Scavenger..."

# Test 1: Basic scan with broken links
echo "Test 1: Basic scan with broken links..."
REPORT=$(bash "$SCRIPT_TO_TEST" "$TEST_DIR")

if echo "$REPORT" | grep -q "[404] https://broken.example.com/404 (found in $TEST_DIR/README.md)" && \
   echo "$REPORT" | grep -q "[500] http://unavailable.example.com/service (found in $TEST_DIR/README.md)" && \
   echo "$REPORT" | grep -q "[404] https://broken-internal.com/doc (found in $TEST_DIR/docs/guide.md)"; then
  echo "Test 1 PASSED: Correctly identified broken links."
else
  echo "Test 1 FAILED: Did not identify all broken links or found extra.\nReport:\n$REPORT"
  exit 1
fi

# Test 2: Scan with ignore patterns
echo "Test 2: Scan with ignore patterns..."
IGNORE_PATTERNS="^https://ignored.example.com/path\n^https://another-ignored.example.com\n^https://broken-internal.com/doc"
REPORT_IGNORED=$(bash "$SCRIPT_TO_TEST" "$TEST_DIR" "$IGNORE_PATTERNS")

if echo "$REPORT_IGNORED" | grep -q "[404] https://broken.example.com/404" && \
   echo "$REPORT_IGNORED" | grep -q "[500] http://unavailable.example.com/service" && \
   ! echo "$REPORT_IGNORED" | grep -q "https://ignored.example.com/path" && \
   ! echo "$REPORT_IGNORED" | grep -q "https://another-ignored.example.com" && \
   ! echo "$REPORT_IGNORED" | grep -q "https://broken-internal.com/doc"; then
  echo "Test 2 PASSED: Correctly ignored specified links."
else
  echo "Test 2 FAILED: Did not correctly apply ignore patterns.\nReport:\n$REPORT_IGNORED"
  exit 1
fi

# Test 3: No broken links (after ignoring all broken ones)
echo "Test 3: No broken links (after ignoring all broken ones)..."
IGNORE_ALL_BROKEN_PATTERNS="^https://broken.example.com/404\n^http://unavailable.example.com/service\n^https://broken-internal.com/doc"
REPORT_NO_BROKEN=$(bash "$SCRIPT_TO_TEST" "$TEST_DIR" "$IGNORE_ALL_BROKEN_PATTERNS")

if [ -z "$REPORT_NO_BROKEN" ]; then
  echo "Test 3 PASSED: No broken links reported when all are ignored."
else
  echo "Test 3 FAILED: Reported broken links when none should be.\nReport:\n$REPORT_NO_BROKEN"
  exit 1
fi

# Test 4: Empty directory scan
echo "Test 4: Empty directory scan..."
mkdir -p "$TEST_DIR/empty_dir"
REPORT_EMPTY=$(bash "$SCRIPT_TO_TEST" "$TEST_DIR/empty_dir")

if [ -z "$REPORT_EMPTY" ]; then
  echo "Test 4 PASSED: No links reported for an empty directory."
else
  echo "Test 4 FAILED: Reported links for an empty directory.\nReport:\n$REPORT_EMPTY"
  exit 1
fi

# Test 5: File with only good links
echo "Test 5: File with only good links..."
cat > "$TEST_DIR/good_links.md" << EOF
# Good Links Only

[Link 1](https://good.example.com/page)
[Link 2](https://redirect.example.com/old)
EOF

REPORT_GOOD_ONLY=$(bash "$SCRIPT_TO_TEST" "$TEST_DIR/good_links.md")

if [ -z "$REPORT_GOOD_ONLY" ]; then
  echo "Test 5 PASSED: No broken links reported for file with only good links."
else
  echo "Test 5 FAILED: Reported broken links for file with only good links.\nReport:\n$REPORT_GOOD_ONLY"
  exit 1
fi


echo "All tests completed successfully."
