#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Setup mock data
cat > "$TMPDIR/installed.txt" <<'EOF'
libc6
linux-image-5.4.0-42-generic
vim
EOF

cat > "$TMPDIR/auto_remove.txt" <<'EOF'
linux-image-5.4.0-42-generic
EOF

# Run script in dry-run mode
output=$("./src/cleanup.sh" -n "$TMPDIR")
# Check output contains expected lines
if ! grep -q "Packages slated for removal: 1" <<<"$output"; then
  echo "Test failed: expected 1 package slated for removal"
  exit 1
fi
if ! grep -q "linux-image-5.4.0-42-generic" <<<"$output"; then
  echo "Test failed: expected package name in list"
  exit 1
fi
if grep -q "Removal simulated" <<<"$output"; then
  echo "Test failed: dry-run should not simulate removal"
  exit 1
fi

# Run script without -n (actual removal)
output=$("./src/cleanup.sh" "$TMPDIR")
if ! grep -q "\[Dry‑run\]" <<<"$output"; then
  echo "Test failed: expected removal simulation message"
  exit 1
fi

# Verify installed.txt no longer contains the removed package
if grep -q "linux-image-5.4.0-42-generic" "$TMPDIR/installed.txt"; then
  echo "Test failed: package not removed from installed.txt"
  exit 1
fi

echo "All tests passed."
