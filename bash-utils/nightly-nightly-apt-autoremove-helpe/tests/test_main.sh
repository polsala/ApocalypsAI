#!/usr/bin/env bash
# Test suite for nightly-apt-autoremove-helper
# ------------------------------------------------------------
# The test creates a temporary directory that contains a mock
# `apt-get` executable. By placing this directory at the front of
# $PATH we ensure the script under test calls the mock instead of the
# real package manager.
# ------------------------------------------------------------

set -euo pipefail

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Mock apt-get that only handles the "-s autoremove" case
cat > "$TMPDIR/apt-get" <<'EOF'
#!/usr/bin/env bash
if [[ "$1" == "-s" && "$2" == "autoremove" ]]; then
  echo "The following packages will be REMOVED:"
  echo "  libfoo1"
  echo "  libbar2"
  echo ""
  echo "0 upgraded, 0 newly installed, 2 to remove and 0 not upgraded."
else
  echo "Mock apt-get called with: $@"
fi
EOF
chmod +x "$TMPDIR/apt-get"

# Prepend the mock directory to PATH
export PATH="$TMPDIR:$PATH"

# Run the utility in dry‑run mode and capture output
output=$(bash src/main.sh --dry-run)

# Expected output (exact match)
expected=$'Packages that would be removed:\n  libfoo1\n  libbar2'

if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Unexpected output"
  echo "Got:"
  echo "$output"
  echo "Expected:"
  echo "$expected"
  exit 1
fi

echo "PASS"
