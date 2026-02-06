#!/usr/bin/env bash
set -euo pipefail

# nightly-apt-cleanup-helper test suite
# ------------------------------------------------------------
# These tests run entirely offline.  They set MOCK_APT=1 to replace
# real apt calls with deterministic mock data.  The test also mocks
# `sudo` to avoid requiring root privileges.
# ------------------------------------------------------------

# Helper to compare multi‑line strings
assert_eq() {
  local got="$1"
  local expected="$2"
  if [[ "$got" != "$expected" ]]; then
    echo "FAIL: output does not match expected"
    echo "--- Got ---"
    echo "$got"
    echo "--- Expected ---"
    echo "$expected"
    exit 1
  fi
}

# -----------------------------------------------------------------
# Test 1: Dry‑run mode (default)
# -----------------------------------------------------------------
export MOCK_APT=1
output=$(bash ../src/main.sh)
expected=$'Packages that would be auto-removed:\nlibfoo\nlibbar\nWould clean apt cache.'
assert_eq "$output" "$expected"

# -----------------------------------------------------------------
# Test 2: Execute mode (mock sudo)
# -----------------------------------------------------------------
# Create a temporary mock `sudo` that just echoes the command
mkdir -p mock_bin
cat > mock_bin/sudo <<'EOF'
#!/usr/bin/env bash
# Mock sudo – simply echo the command for testing purposes
echo "sudo $@"
EOF
chmod +x mock_bin/sudo
export PATH="$(pwd)/mock_bin:$PATH"

output=$(bash ../src/main.sh --execute)
expected=$'Running autoremove...\nsudo apt-get -y autoremove\nCleaning apt cache...\nsudo apt-get clean'
assert_eq "$output" "$expected"

# Clean up mock binary
rm -rf mock_bin

echo "All tests passed"
