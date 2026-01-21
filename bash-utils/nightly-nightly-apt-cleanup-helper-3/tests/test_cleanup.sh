#!/usr/bin/env bash

# Tests for nightly-apt-cleanup-helper
# These tests are deterministic and do not touch the real system.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
SCRIPT="$PROJECT_ROOT/src/cleanup.sh"

# Helper to run the script and capture output
run_script() {
  local args=($@)
  "$SCRIPT" "${args[@]}" 2>&1
}

# Create a temporary package list file
TMP_FILE=$(mktemp)
cat > "$TMP_FILE" <<'EOF'
unused-lib1
unused-lib2
EOF

# Test 1: Listing packages
OUTPUT=$(run_script --list --file "$TMP_FILE")
if [[ "$OUTPUT" != *"unused-lib1"* ]] || [[ "$OUTPUT" != *"unused-lib2"* ]]; then
  echo "Test 1 FAILED: Expected package names in list output"
  echo "Output was:"
  echo "$OUTPUT"
  exit 1
fi

echo "Test 1 PASSED"

# Test 2: Dry‑run clean
OUTPUT=$(run_script --clean --dry-run --file "$TMP_FILE")
if [[ "$OUTPUT" != *"Dry‑run mode: would execute"* ]] || [[ "$OUTPUT" != *"unused-lib1"* ]] || [[ "$OUTPUT" != *"unused-lib2"* ]]; then
  echo "Test 2 FAILED: Expected dry‑run command with package names"
  echo "Output was:"
  echo "$OUTPUT"
  exit 1
fi

echo "Test 2 PASSED"

# Cleanup
rm -f "$TMP_FILE"

# Note: We do NOT test the real --clean path to avoid system changes.

exit 0
