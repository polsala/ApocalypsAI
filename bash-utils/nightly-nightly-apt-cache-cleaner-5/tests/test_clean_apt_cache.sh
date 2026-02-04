#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: use a temporary directory to avoid touching the real APT cache.
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Create mock .deb files (package_version_arch.deb)
# foo has two versions; bar has a single version.
 touch "$TMPDIR/foo_1.0_amd64.deb"
 touch "$TMPDIR/foo_1.1_amd64.deb"
 touch "$TMPDIR/bar_2.0_amd64.deb"

# Run in dry‑run mode and capture output
output=$(bash ../../src/clean_apt_cache.sh 2>/dev/null)
if [[ "$output" != *"Would delete: $TMPDIR/foo_1.0_amd64.deb"* ]]; then
  echo "Dry‑run test failed: expected old foo package to be listed for deletion"
  exit 1
fi

# Run actual deletion
bash ../../src/clean_apt_cache.sh -y

# Verify that only the newest foo package remains and bar is untouched
if [[ -e "$TMPDIR/foo_1.0_amd64.deb" ]]; then
  echo "Deletion test failed: old foo package still exists"
  exit 1
fi
if [[ ! -e "$TMPDIR/foo_1.1_amd64.deb" ]]; then
  echo "Deletion test failed: newest foo package missing"
  exit 1
fi
if [[ ! -e "$TMPDIR/bar_2.0_amd64.deb" ]]; then
  echo "Deletion test failed: single‑version bar package missing"
  exit 1
fi

echo "All tests passed"
