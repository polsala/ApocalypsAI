#!/usr/bin/env bash
set -euo pipefail

# Helper function for assertions
assert_contains() {
  local text="$1"
  local pattern="$2"
  if ! grep -q "$pattern" <<<"$text"; then
    echo "Assertion failed: expected pattern '$pattern' not found."
    exit 1
  fi
}

# Setup temporary cache directory
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Create test .deb files with different ages
# old1.deb – very old (Jan 1 2022)
# old2.deb – old (Jan 1 2023)
# new.deb  – current time

touch -t 202201010000 "$TMPDIR/old1.deb"

touch -t 202301010000 "$TMPDIR/old2.deb"

touch -t $(date +%Y%m%d%H%M) "$TMPDIR/new.deb"

# -------------------------------------------------------------------
# Dry‑run test: use a very large DAYS value so both old files are selected
# -------------------------------------------------------------------
OUTPUT=$(bash ../src/apt-cache-cleaner.sh -d -n 3650)

assert_contains "$OUTPUT" "old1.deb"
assert_contains "$OUTPUT" "old2.deb"
# Ensure new.deb is NOT listed
if grep -q "new.deb" <<<"$OUTPUT"; then
  echo "Assertion failed: new.deb should not appear in dry run output."
  exit 1
fi

# -------------------------------------------------------------------
# Actual deletion test
# -------------------------------------------------------------------
bash ../src/apt-cache-cleaner.sh -n 3650

# Verify old files are gone, new remains
if [[ -e "$TMPDIR/old1.deb" || -e "$TMPDIR/old2.deb" ]]; then
  echo "Assertion failed: old files were not deleted."
  exit 1
fi
if [[ ! -e "$TMPDIR/new.deb" ]]; then
  echo "Assertion failed: new.deb should not be deleted."
  exit 1
fi

echo "All tests passed."
