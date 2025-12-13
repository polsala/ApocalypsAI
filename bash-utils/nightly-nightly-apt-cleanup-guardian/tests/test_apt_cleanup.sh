#!/usr/bin/env bash
# Test suite for nightly-apt-cleanup-guardian

set -euo pipefail

# Mock rationale: Use a temporary directory to simulate the APT cache.
TMP_CACHE=$(mktemp -d)
export APT_CACHE_DIR="$TMP_CACHE"

# Create dummy .deb files with specific timestamps
touch -t 202001010000 "$TMP_CACHE/old-package-1.deb"   # very old
touch -t 202301010000 "$TMP_CACHE/old-package-2.deb"   # older than 30 days
touch -t "$(date +%Y%m%d%H%M)" "$TMP_CACHE/fresh-package.deb" # now

# Run script in dry‑run mode, keep days = 30
OUTPUT=$(bash ../src/apt-cleanup.sh --dry-run --keep-days=30)

# Expect both old files to be listed, fresh file not listed
if ! grep -q "old-package-1.deb" <<< "$OUTPUT"; then
  echo "FAIL: old-package-1.deb not reported"
  exit 1
fi
if ! grep -q "old-package-2.deb" <<< "$OUTPUT"; then
  echo "FAIL: old-package-2.deb not reported"
  exit 1
fi
if grep -q "fresh-package.deb" <<< "$OUTPUT"; then
  echo "FAIL: fresh-package.deb should not be reported"
  exit 1
fi

# Now run actual deletion
bash ../src/apt-cleanup.sh --keep-days=30

# Verify old files are gone, fresh remains
if [[ -e "$TMP_CACHE/old-package-1.deb" ]] || [[ -e "$TMP_CACHE/old-package-2.deb" ]]; then
  echo "FAIL: old files were not deleted"
  exit 1
fi
if [[ ! -e "$TMP_CACHE/fresh-package.deb" ]]; then
  echo "FAIL: fresh file was incorrectly deleted"
  exit 1
fi

echo "All tests passed."
