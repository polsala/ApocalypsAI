#!/usr/bin/env bash

# Mock rationale: All tests run in a temporary directory with a fake apt cache.
# This ensures they are deterministic and offline.

set -euo pipefail

# Load the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
source "$SCRIPT_DIR/cleanup.sh"

# Helper to create a .deb file with a specific modification time (in days ago)
create_deb() {
  local dir="$1" name="$2" days_ago="$3"
  local path="$dir/$name.deb"
  touch "$path"
  # Adjust mtime
  local timestamp=$(date -d "-$days_ago days" +"%Y%m%d%H%M.%S")
  touch -t "$timestamp" "$path"
}

# Assertion helpers
assert_file_exists() {
  local file="$1"
  if [[ ! -e "$file" ]]; then
    echo "Assertion failed: expected file '$file' to exist" >&2
    exit 1
  fi
}

assert_file_not_exists() {
  local file="$1"
  if [[ -e "$file" ]]; then
    echo "Assertion failed: expected file '$file' to be removed" >&2
    exit 1
  fi
}

# Begin tests
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Create test files: recent (2 days old) and old (10 days old)
create_deb "$TMPDIR" "recent" 2
create_deb "$TMPDIR" "old" 10

# ---------- Dry‑run test ----------
# Capture output
DRY_OUTPUT=$(bash "$SCRIPT_DIR/cleanup.sh" --dry-run --max-age-days 5)
# Expect "old.deb" to be listed, "recent.deb" not listed
if ! echo "$DRY_OUTPUT" | grep -q "old.deb"; then
  echo "Dry‑run test failed: 'old.deb' not reported" >&2
  exit 1
fi
if echo "$DRY_OUTPUT" | grep -q "recent.deb"; then
  echo "Dry‑run test failed: 'recent.deb' should not be reported" >&2
  exit 1
fi

# ---------- Real cleanup test ----------
bash "$SCRIPT_DIR/cleanup.sh" --max-age-days 5
assert_file_not_exists "$TMPDIR/old.deb"
assert_file_exists "$TMPDIR/recent.deb"

# ---------- Custom max‑age test (3 days) ----------
# Re‑create old file with 4‑day age
create_deb "$TMPDIR" "old2" 4
bash "$SCRIPT_DIR/cleanup.sh" --max-age-days 3
assert_file_not_exists "$TMPDIR/old2.deb"

# Cleanup temporary directory
rm -rf "$TMPDIR"

echo "All tests passed."
