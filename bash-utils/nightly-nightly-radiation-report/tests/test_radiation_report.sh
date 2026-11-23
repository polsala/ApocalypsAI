#!/usr/bin/env bash

# Test suite for nightly-radiation-report
# Uses only built‑in tools; no external network calls.
# Mock rationale: none needed – the script is fully deterministic.

set -euo pipefail

# Resolve script path relative to this test file
SCRIPT_PATH="$(dirname "$0")/../src/radiation_report.sh"

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Prepare a known test file
TESTFILE="$TMPDIR/test.txt"
cat >"$TESTFILE" <<'EOF'
Apocalypse is near.
Stay safe.
EOF

# Run the utility
OUTPUT=$(bash "$SCRIPT_PATH" "$TESTFILE")

# Verify header line
if [[ "$OUTPUT" != *"Radiation Report for $TESTFILE"* ]]; then
  echo "Header line missing or incorrect"
  exit 1
fi

# Verify size line exists
if ! echo "$OUTPUT" | grep -q "Size:"; then
  echo "Size line missing"
  exit 1
fi

# Verify line count (should be 2)
if ! echo "$OUTPUT" | grep -q "Lines: 2"; then
  echo "Incorrect line count"
  exit 1
fi

# Extract radiation level and ensure it is a number between 0 and 100
RADIATION=$(echo "$OUTPUT" | grep "Radiation Level:" | awk '{print $3}')
if ! [[ "$RADIATION" =~ ^[0-9]+$ ]]; then
  echo "Radiation level is not numeric"
  exit 1
fi
if (( RADIATION < 0 || RADIATION > 100 )); then
  echo "Radiation level out of expected range"
  exit 1
fi

echo "All tests passed."
