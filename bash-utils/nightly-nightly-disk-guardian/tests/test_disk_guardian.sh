#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Helper to create a mock df that returns a given usage percent
create_mock_df() {
  local usage_percent=$1
  cat > "$ROOT_DIR/mock_bin/df" <<EOS
#!/usr/bin/env bash
cat <<'MOCK'
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        20G   18G  2.0G  ${usage_percent}% /
MOCK
EOS
  chmod +x "$ROOT_DIR/mock_bin/df"
}

mkdir -p "$ROOT_DIR/mock_bin"
export PATH="$ROOT_DIR/mock_bin:$PATH"

# ---- Test high usage (should warn) ----
create_mock_df 90
output=$("$SCRIPT_DIR/../src/disk_guardian.sh" 2>&1) || exit_code=$?
exit_code=$?
if [[ $exit_code -ne 1 ]]; then
  echo "High usage: expected exit code 1, got $exit_code"
  exit 1
fi
if [[ $output != *"LOW SPACE"* ]]; then
  echo "High usage: expected warning message, got:"
  echo "$output"
  exit 1
fi

# ---- Test low usage (should be OK) ----
create_mock_df 30
output=$("$SCRIPT_DIR/../src/disk_guardian.sh" 2>&1) || exit_code=$?
exit_code=$?
if [[ $exit_code -ne 0 ]]; then
  echo "Low usage: expected exit code 0, got $exit_code"
  exit 1
fi
if [[ $output != *"✅"* ]]; then
  echo "Low usage: expected success message, got:"
  echo "$output"
  exit 1
fi

echo "All tests passed."
