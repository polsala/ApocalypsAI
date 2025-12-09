#!/usr/bin/env bash
# Test for nightly-emoji-qr
# Mock rationale: deterministic input "AB" should produce a known emoji grid.
set -e

EXPECTED=$'😃😄\n😀😀'

OUTPUT=$(node src/index.js "AB")

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "✅ test passed"
  exit 0
else
  echo "❌ test failed"
  echo "Expected:"
  echo "$EXPECTED"
  echo "Got:"
  echo "$OUTPUT"
  exit 1
fi
