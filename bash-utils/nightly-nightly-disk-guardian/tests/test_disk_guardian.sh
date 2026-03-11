#!/usr/bin/env bash
set -euo pipefail

# Test script for nightly-disk-guardian
# Uses a mock `df` to provide deterministic output.

# Create a temporary directory for the mock binary
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Write the mock `df` script
cat > "$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df output for specific mount points
if [[ "$1" == "/" ]]; then
  cat <<EOD
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   41G   9G   82% /
EOD
elif [[ "$1" == "/home" ]]; then
  cat <<EOD
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       100G   60G   40G   60% /home
EOD
else
  # Default empty output for unknown mounts
  echo "Filesystem      Size  Used Avail Use% Mounted on"
fi
EOF
chmod +x "$TMPDIR/df"

# Prepend the mock directory to PATH so our script uses it
export PATH="$TMPDIR:$PATH"

# Run the utility with a low threshold to trigger a warning for `/`
output=$(../src/disk-guardian.sh -t 80 / /home)

# Expect a warning line for `/`
if [[ "$output" != *"Warning! / is at 82%"* ]]; then
  echo "Test failed: expected warning for '/' mount"
  exit 1
fi

# Ensure no warning appears for `/home` (usage 60% < 80%)
if [[ "$output" == *"Warning! /home"* ]]; then
  echo "Test failed: unexpected warning for '/home' mount"
  exit 1
fi

echo "All tests passed."
