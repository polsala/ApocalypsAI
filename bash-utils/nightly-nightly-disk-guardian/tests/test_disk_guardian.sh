#!/usr/bin/env bash
set -euo pipefail

# Helper to create a temporary mock `df` that returns the given usage percentage
create_mock_df() {
  local usage_percent="$1"
  local mock_dir="$2"
  cat > "${mock_dir}/df" <<MOCK
#!/usr/bin/env bash
cat <<OUTPUT
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G   16G  4.0G  ${usage_percent}% /
OUTPUT
MOCK
  chmod +x "${mock_dir}/df"
}

# ---------- Test 1: Usage equals threshold (no alert) ----------
TMPDIR1=$(mktemp -d)
create_mock_df 80 "$TMPDIR1"
PATH="$TMPDIR1:$PATH"
output=$(bash ../src/disk_guardian.sh 80 2>&1) && status=$? || status=$?
if [[ $status -ne 0 ]]; then
  echo "Test 1 failed: expected exit 0, got $status"
  exit 1
fi
if [[ $output != *"All is calm."* ]]; then
  echo "Test 1 failed: expected calm message"
  exit 1
fi
# Clean up mock
rm -rf "$TMPDIR1"

# ---------- Test 2: Usage exceeds threshold (alert) ----------
TMPDIR2=$(mktemp -d)
create_mock_df 85 "$TMPDIR2"
PATH="$TMPDIR2:$PATH"
output=$(bash ../src/disk_guardian.sh 70 2>&1) && status=$? || status=$?
if [[ $status -ne 1 ]]; then
  echo "Test 2 failed: expected exit 1, got $status"
  exit 1
fi
if [[ $output != *"Guardian says"* ]]; then
  echo "Test 2 failed: expected guardian ASCII art"
  exit 1
fi
# Clean up mock
rm -rf "$TMPDIR2"

echo "All tests passed."
