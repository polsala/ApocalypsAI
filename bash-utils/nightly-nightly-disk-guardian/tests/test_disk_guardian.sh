#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/../src/disk_guardian.sh"

# Test case: below threshold
DF_OUTPUT="30%" bash "$SRC" 80 >out.txt
status=$?
if [[ $status -ne 0 ]]; then
  echo "Expected exit 0 for low usage"
  exit 1
fi
if ! grep -q "✅ Disk usage at 30% is within safe limits." out.txt; then
  echo "Missing success message"
  exit 1
fi

# Test case: above threshold
DF_OUTPUT="90%" bash "$SRC" 80 >out.txt 2>&1
status=$?
if [[ $status -ne 1 ]]; then
  echo "Expected exit 1 for high usage"
  exit 1
fi
if ! grep -q "Disk usage" out.txt; then
  echo "Missing warning message"
  exit 1
fi

echo "All tests passed"
