#!/usr/bin/env bash

set -e

# ---------------------------------------------------------------------------
# Setup a temporary directory that will shadow the real PATH with a mock
# `apt-get` binary. This ensures the test never touches the host system's
# package manager.
# ---------------------------------------------------------------------------
TMPDIR=$(mktemp -d)
export PATH="$TMPDIR:$PATH"

# Create a mock `apt-get` that records its arguments to a log file.
cat > "$TMPDIR/apt-get" <<'EOF'
#!/usr/bin/env bash
# Mock apt-get – simply log the arguments and simulate output.
log_file="${TMPDIR}/apt-log.txt"
echo "apt-get called with: $@" >> "$log_file"
if [[ "$*" == *"--dry-run"* ]]; then
  echo "Would remove: package1 package2"
else
  echo "Removing: package1 package2"
fi
EOF
chmod +x "$TMPDIR/apt-get"

# ---------------------------------------------------------------------------
# Execute the utility in dry‑run mode and verify the mock was invoked correctly.
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
"$SCRIPT_DIR/cleanup.sh" --dry-run

if ! grep -q "apt-get called with: autoremove --dry-run -y" "$TMPDIR/apt-log.txt"; then
  echo "Test failed: dry‑run invocation not recorded"
  exit 1
fi

# ---------------------------------------------------------------------------
# Execute the utility without the dry‑run flag (actual removal) and verify.
# ---------------------------------------------------------------------------
"$SCRIPT_DIR/cleanup.sh"

if ! grep -q "apt-get called with: autoremove -y" "$TMPDIR/apt-log.txt"; then
  echo "Test failed: actual removal invocation not recorded"
  exit 1
fi

# ---------------------------------------------------------------------------
# Clean up temporary files and report success.
# ---------------------------------------------------------------------------
rm -rf "$TMPDIR"

echo "All tests passed"
