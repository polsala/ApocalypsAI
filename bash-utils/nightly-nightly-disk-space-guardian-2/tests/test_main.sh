#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory to hold mock binaries
MOCK_BIN=$(mktemp -d)
export PATH="$MOCK_BIN:$PATH"

# Helper to create a mock df script with given output
create_mock_df() {
  cat > "$MOCK_BIN/df" <<'EOS'
#!/usr/bin/env bash
cat <<EOF
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G   12G   8G  60% /
EOF
EOS
  chmod +x "$MOCK_BIN/df"
}

# Test: usage below threshold (default 80%)
create_mock_df
output=$(bash ../../src/main.sh -t 70)
if [[ "$output" != *"All good"* ]]; then
  echo "Test failed: expected All good message when usage is 60%"
  exit 1
fi

# Update mock df to simulate high usage
cat > "$MOCK_BIN/df" <<'EOS'
#!/usr/bin/env bash
cat <<EOF
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G   18G   2G  90% /
EOF
EOS
chmod +x "$MOCK_BIN/df"

# Prepare a temporary TMPDIR with an old file for cleanup test
TMPDIR=$(mktemp -d)
export TMPDIR
old_file="$TMPDIR/oldfile"
touch "$old_file"
# Set modification time to >1 day ago
touch -d "2 days ago" "$old_file"

# Override find to operate within our TMPDIR only (safety)
find() {
  command find "$TMPDIR" "$@"
}
export -f find

# Test: usage above threshold with cleanup flag
output=$(bash ../../src/main.sh -t 80 -c)
if [[ "$output" != *"Cleaning $TMPDIR files older than 1 day"* ]]; then
  echo "Test failed: expected cleanup message when usage is 90%"
  exit 1
fi

# Verify that the old file was deleted
if [[ -e "$old_file" ]]; then
  echo "Test failed: old file was not deleted during cleanup"
  exit 1
fi

echo "All tests passed."
