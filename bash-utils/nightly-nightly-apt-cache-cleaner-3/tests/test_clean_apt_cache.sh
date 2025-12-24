#!/usr/bin/env bash
set -euo pipefail

# ---- Test Setup -----------------------------------------------------------
# Create a temporary directory to act as a mock APT cache
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Helper to create a file with a specific timestamp (format: YYYYMMDDhhmm)
create_file() {
  local name="$1"
  local timestamp="$2"
  touch -t "$timestamp" "$TMPDIR/$name"
}

# Create files: two old, one recent
# Old files: Jan 1 2020 and Dec 1 2020
create_file "old1.deb" "202001010000"
create_file "old2.deb" "202012010000"
# Recent file: current date/time
CURRENT_TS=$(date +%Y%m%d%H%M)
create_file "new.deb" "$CURRENT_TS"

# ---- Dry‑run Test ----------------------------------------------------------
# Use a large threshold (365 days) so the two old files qualify
DRY_OUTPUT=$(bash src/clean_apt_cache.sh -d 365 -n)

# Verify that the dry‑run reports the two old files and not the recent one
if ! grep -q "Would delete: $TMPDIR/old1.deb" <<<"$DRY_OUTPUT"; then
  echo "FAIL: old1.deb not reported in dry‑run"
  exit 1
fi
if ! grep -q "Would delete: $TMPDIR/old2.deb" <<<"$DRY_OUTPUT"; then
  echo "FAIL: old2.deb not reported in dry‑run"
  exit 1
fi
if grep -q "Would delete: $TMPDIR/new.deb" <<<"$DRY_OUTPUT"; then
  echo "FAIL: new.deb incorrectly reported in dry‑run"
  exit 1
fi

# ---- Actual Deletion Test -------------------------------------------------
# Run the script without -n to perform real deletions
bash src/clean_apt_cache.sh -d 365

# old files should be gone, new file should remain
if [[ -e "$TMPDIR/old1.deb" ]] || [[ -e "$TMPDIR/old2.deb" ]]; then
  echo "FAIL: old files were not deleted"
  exit 1
fi
if [[ ! -e "$TMPDIR/new.deb" ]]; then
  echo "FAIL: new file was incorrectly deleted"
  exit 1
fi

echo "All tests passed"
