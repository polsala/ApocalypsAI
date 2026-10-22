#!/bin/bash

# Mock rationale: This test script directly calls the bless_release.sh script.
# Instead of relying on the GitHub Actions runtime to set environment variables,
# we explicitly set BLESSING_TYPE for each test case. This ensures deterministic
# behavior and allows the tests to run offline without any external dependencies.
# The 'RANDOM' variable is inherently non-deterministic, but for testing the
# *structure* and *content presence* of the output, it's sufficient to ensure
# that *a* blessing and *a* tip are generated and conform to expectations.
# We are not testing the randomness itself, but the script's ability to produce
# valid output given different BLESSING_TYPE inputs.

SCRIPT_PATH="$(dirname "$0")"/../src/bless_release.sh

echo "Running tests for bless_release.sh"

# Test 1: Default (random) blessing type
echo "Test 1: Default (random) blessing type"
unset BLESSING_TYPE # Ensure it defaults
OUTPUT=$(bash "$SCRIPT_PATH")
if [[ "$OUTPUT" == *"--- Nightly Release Blessing ---"* && \
      "$OUTPUT" == *"--- Survival Tip of the Cycle ---"* && \
      "$OUTPUT" == *"May your deployments be swift and your uptime eternal."* ]]; then
  echo "  PASS: Output contains expected headers and footer."
else
  echo "  FAIL: Output missing expected headers/footer for random type."
  echo "Output was: $OUTPUT"
  exit 1
fi

# Test 2: Ominous blessing type
echo "Test 2: Ominous blessing type"
OUTPUT=$(BLESSING_TYPE="ominous" bash "$SCRIPT_PATH")
if [[ "$OUTPUT" == *"--- Nightly Release Blessing ---"* && \
      "$OUTPUT" == *"--- Survival Tip of the Cycle ---"* ]]; then
  echo "  PASS: Output contains expected headers for ominous type."
else
  echo "  FAIL: Output missing expected headers for ominous type."
  echo "Output was: $OUTPUT"
  exit 1
fi

# Test 3: Hopeful blessing type
echo "Test 3: Hopeful blessing type"
OUTPUT=$(BLESSING_TYPE="hopeful" bash "$SCRIPT_PATH")
if [[ "$OUTPUT" == *"--- Nightly Release Blessing ---"* && \
      "$OUTPUT" == *"--- Survival Tip of the Cycle ---"* ]]; then
  echo "  PASS: Output contains expected headers for hopeful type."
else
  echo "  FAIL: Output missing expected headers for hopeful type."
  echo "Output was: $OUTPUT"
  exit 1
fi

# Test 4: Invalid blessing type should default to random
echo "Test 4: Invalid blessing type defaults to random"
OUTPUT=$(BLESSING_TYPE="apocalyptic_chaos" bash "$SCRIPT_PATH")
if [[ "$OUTPUT" == *"--- Nightly Release Blessing ---"* && \
      "$OUTPUT" == *"--- Survival Tip of the Cycle ---"* ]]; then
  echo "  PASS: Output contains expected headers for invalid type (defaulted to random)."
else
  echo "  FAIL: Output missing expected headers for invalid type."
  echo "Output was: $OUTPUT"
  exit 1
fi

echo "All tests passed for bless_release.sh"
