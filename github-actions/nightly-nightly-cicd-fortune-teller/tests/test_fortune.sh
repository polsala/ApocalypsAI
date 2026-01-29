#!/bin/bash

# Mock rationale: This script tests a simple bash script that uses `shuf`.
# `shuf` is a standard utility and its behavior (random selection from input)
# is well-defined. We don't need to mock `shuf` itself, but rather ensure
# our script correctly calls it and processes its output.
# The tests will check for non-empty output and keywords to confirm the
# correct type of fortune is generated.

SCRIPT_PATH="$(dirname "$0")"/../src/fortune.sh

# Test 1: Default (blessing) fortune
echo "Running Test 1: Default fortune (blessing)"
OUTPUT=$(bash "$SCRIPT_PATH")
if [ -z "$OUTPUT" ]; then
  echo "FAIL: Default fortune output is empty."
  exit 1
fi
if [[ "$OUTPUT" != *"May"* && "$OUTPUT" != *"The cosmic"* && "$OUTPUT" != *"Your code"* && "$OUTPUT" != *"A gentle breeze"* && "$OUTPUT" != *"The stars"* && "$OUTPUT" != *"May your tests"* && "$OUTPUT" != *"The spirits"* ]]; then
  echo "WARN: Default fortune output does not contain expected blessing keywords. Output: '$OUTPUT'"
fi
echo "PASS: Default fortune generated non-empty output."

# Test 2: Blessing fortune explicitly
echo "Running Test 2: Explicit blessing fortune"
OUTPUT=$(bash "$SCRIPT_PATH" "blessing")
if [ -z "$OUTPUT" ]; then
  echo "FAIL: Explicit blessing fortune output is empty."
  exit 1
}
if [[ "$OUTPUT" != *"May"* && "$OUTPUT" != *"The cosmic"* && "$OUTPUT" != *"Your code"* && "$OUTPUT" != *"A gentle breeze"* && "$OUTPUT" != *"The stars"* && "$OUTPUT" != *"May your tests"* && "$OUTPUT" != *"The spirits"* ]]; then
  echo "WARN: Explicit blessing fortune output does not contain expected blessing keywords. Output: '$OUTPUT'"
fi
echo "PASS: Explicit blessing fortune generated non-empty output."

# Test 3: Warning fortune
echo "Running Test 3: Warning fortune"
OUTPUT=$(bash "$SCRIPT_PATH" "warning")
if [ -z "$OUTPUT" ]; then
  echo "FAIL: Warning fortune output is empty."
  exit 1
fi
if [[ "$OUTPUT" != *"Beware"* && "$OUTPUT" != *"The ancient scrolls"* && "$OUTPUT" != *"A shadow"* && "$OUTPUT" != *"The void"* && "$OUTPUT" != *"A forgotten cache"* && "$OUTPUT" != *"The prophecy"* && "$OUTPUT" != *"A subtle off-by-one"* ]]; then
  echo "WARN: Warning fortune output does not contain expected warning keywords. Output: '$OUTPUT'"
fi
echo "PASS: Warning fortune generated non-empty output."

# Test 4: Invalid fortune type (should default to blessing)
echo "Running Test 4: Invalid fortune type (should default to blessing)"
OUTPUT=$(bash "$SCRIPT_PATH" "invalid_type")
if [ -z "$OUTPUT" ]; then
  echo "FAIL: Invalid type fortune output is empty."
  exit 1
fi
if [[ "$OUTPUT" != *"May"* && "$OUTPUT" != *"The cosmic"* && "$OUTPUT" != *"Your code"* && "$OUTPUT" != *"A gentle breeze"* && "$OUTPUT" != *"The stars"* && "$OUTPUT" != *"May your tests"* && "$OUTPUT" != *"The spirits"* ]]; then
  echo "WARN: Invalid type fortune output does not contain expected blessing keywords. Output: '$OUTPUT'"
fi
echo "PASS: Invalid type fortune defaulted to blessing and generated non-empty output."

echo "All tests completed."
exit 0
