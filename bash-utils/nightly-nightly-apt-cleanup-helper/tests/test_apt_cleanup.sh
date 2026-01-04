#!/usr/bin/env bash

set -e

# Create a temporary directory for the mock and logs
TMPDIR=$(mktemp -d)
MOCK_LOG="$TMPDIR/apt_log.txt"

# Mock apt-get that records its arguments
cat > "$TMPDIR/apt-get" <<'EOF'
#!/usr/bin/env bash
# Record the call for verification
echo "apt-get called with: $@" >> "$MOCK_LOG"
exit 0
EOF
chmod +x "$TMPDIR/apt-get"

# Prepend mock directory to PATH so the script uses it
export PATH="$TMPDIR:$PATH"
# Provide deterministic output for dry‑run mode
export MOCK_APT_GET_OUTPUT="Simulated autoremove output\nSimulated clean output"

# ---------- Dry‑run test ----------
./src/apt_cleanup.sh --dry-run > "$TMPDIR/dry_output.txt"
# Ensure the mock was NOT invoked
if grep -q "apt-get called" "$MOCK_LOG"; then
  echo "Dry run should not invoke apt-get" >&2
  exit 1
fi
# Verify the simulated output appears
if ! grep -q "Simulated autoremove output" "$TMPDIR/dry_output.txt"; then
  echo "Dry run output missing simulated data" >&2
  exit 1
fi

# ---------- Execute test ----------
./src/apt_cleanup.sh --execute > "$TMPDIR/exec_output.txt"
# Verify that autoremove was called
if ! grep -q "apt-get called with: -y autoremove" "$MOCK_LOG"; then
  echo "Execute mode did not call autoremove" >&2
  exit 1
fi
# Verify that clean was called
if ! grep -q "apt-get called with: clean" "$MOCK_LOG"; then
  echo "Execute mode did not call clean" >&2
  exit 1
fi

echo "All tests passed"
