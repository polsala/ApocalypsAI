#!/usr/bin/env bash

# Test harness for nightly-disk-guardian

set -e

# Helper to run script with mocked df
run_with_mock() {
  local mock_usage="$1"
  local threshold="${2:-}"
  tmpdir=$(mktemp -d)
  cat > "$tmpdir/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: prints provided header and usage line
echo "Filesystem      Size  Used Avail Use% Mounted on"
echo "/dev/root        20G   12G   8G  ${MOCK_USAGE}% /"
EOF
  chmod +x "$tmpdir/df"
  export PATH="$tmpdir:$PATH"
  export MOCK_USAGE="$mock_usage"
  if [ -z "$threshold" ]; then
    bash ../../src/disk_guardian.sh
  else
    bash ../../src/disk_guardian.sh "$threshold"
  fi
  local status=$?
  echo "STATUS=$status"
  rm -rf "$tmpdir"
  return $status
}

# Test 1: usage above threshold
output=$(run_with_mock 85 80 2>&1) && status=$? || status=$?
if [[ $status -ne 1 ]]; then
  echo "Test 1 failed: expected exit 1"
  exit 1
fi
if ! echo "$output" | grep -q "monster"; then
  echo "Test 1 failed: expected monster ASCII"
  exit 1
fi

# Test 2: usage below threshold
output=$(run_with_mock 45 80 2>&1) && status=$? || status=$?
if [[ $status -ne 0 ]]; then
  echo "Test 2 failed: expected exit 0"
  exit 1
fi
if ! echo "$output" | grep -q "sun"; then
  echo "Test 2 failed: expected sun ASCII"
  exit 1
fi

echo "All tests passed."
