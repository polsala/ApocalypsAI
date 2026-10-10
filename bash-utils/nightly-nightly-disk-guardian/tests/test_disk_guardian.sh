#!/usr/bin/env bash

# test_disk_guardian.sh – test suite for nightly-disk-guardian

set -euo pipefail

# Directory of this script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Path to the utility script
UTIL="$SCRIPT_DIR/../src/disk-guardian.sh"

# Create a temporary directory for a mock 'df' command
TMPDIR=$(mktemp -d)

cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Mock df that returns a fixed usage of 78%
cat > "$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df – always reports 78% usage for root
if [[ "$1" == "/" ]]; then
  echo "Filesystem      Size  Used Avail Use% Mounted on"
  echo "/dev/mock       50G   39G   11G  78% /"
else
  /bin/df "$@"
fi
EOF
chmod +x "$TMPDIR/df"

# Prepend the mock directory to PATH so our script picks it up
export PATH="$TMPDIR:$PATH"

# Run the utility with a low threshold to force a warning
OUTPUT=$($UTIL 50)

# Expected warning prefix
if [[ "$OUTPUT" != ⚠️* ]]; then
  echo "Test failed: Expected warning output, got: $OUTPUT"
  exit 1
fi

# Ensure the usage percentage reported matches the mock (78%)
if [[ "$OUTPUT" != *"78%"* ]]; then
  echo "Test failed: Expected usage 78% in output, got: $OUTPUT"
  exit 1
fi

# Run the utility with a high threshold to ensure safe message
OUTPUT_SAFE=$($UTIL 90)
if [[ "$OUTPUT_SAFE" != ✅* ]]; then
  echo "Test failed: Expected safe output, got: $OUTPUT_SAFE"
  exit 1
fi

echo "All tests passed."
