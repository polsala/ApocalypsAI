#!/bin/sh

set -e

# Fixed seed to make the output predictable
export SEED=12345

# Run the script directly (no Docker needed for the test)
OUTPUT=$(../src/fortune.sh)

# With SEED=12345 and 5 fortunes, the index calculation yields:
# INDEX = (12345 % 5) + 1 = (0) + 1 = 1
EXPECTED="You will find a hidden stash of canned beans."

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED' but got '$OUTPUT'"
  exit 1
fi
