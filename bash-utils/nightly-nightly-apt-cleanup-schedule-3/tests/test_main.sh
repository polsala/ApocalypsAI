#!/usr/bin/env bash
set -euo pipefail

# tests for nightly-apt-cleanup-scheduler.sh
# Mock rationale: we replace sudo and apt-get with harmless echo commands
# and simulate a cache directory with temporary files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/main.sh"

# Create temporary cache directory
TMP_CACHE=$(mktemp -d)
export APTCACHE_DIR="$TMP_CACHE"

# Populate with mock files
touch "$TMP_CACHE/old_pkg1.deb"
touch "$TMP_CACHE/new_pkg2.deb"
# Set modification times: old_pkg1 8 days ago, new_pkg2 today
touch -d "8 days ago" "$TMP_CACHE/old_pkg1.deb"

# Mock sudo and apt-get
FAKE_BIN_DIR=$(mktemp -d)
export PATH="$FAKE_BIN_DIR:$PATH"

cat > "$FAKE_BIN_DIR/sudo" <<'EOF'
#!/usr/bin/env bash
exec "$@"
EOF
chmod +x "$FAKE_BIN_DIR/sudo"

cat > "$FAKE_BIN_DIR/apt-get" <<'EOF'
#!/usr/bin/env bash
echo "apt-get $@"
EOF
chmod +x "$FAKE_BIN_DIR/apt-get"

# Run script in dry-run mode
OUTPUT=$("$SCRIPT_PATH" --dry-run 2>&1)

# Check that old package is listed and no cleaning occurs
if [[ "$OUTPUT" != *"old_pkg1.deb"* ]]; then
    echo "Test failed: old package not listed"
    exit 1
fi
if [[ "$OUTPUT" == *"apt-get clean"* ]]; then
    echo "Test failed: apt-get should not be called in dry-run"
    exit 1
fi

echo "All tests passed."
