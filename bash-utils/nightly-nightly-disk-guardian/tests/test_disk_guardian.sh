#!/usr/bin/env bash
set -euo pipefail

# Directory of this test script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTIL_SCRIPT="$DIR/../src/disk_guardian.sh"

run_test() {
  local name=$1
  local mock_usage=$2   # e.g., "85"
  local threshold=$3    # e.g., "80"
  local expect_warn=$4  # "yes" or "no"

  # Create temporary directory for mock commands
  TMPDIR=$(mktemp -d)
  # Mock df command that ignores its arguments and prints a fixed line
  cat >"$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: output a header and a usage line using the MOCK_USAGE env var
echo "Filesystem 1024-blocks Used Available Capacity Mounted on"
echo "mockfs 1000000 850000 150000 ${MOCK_USAGE}% /mock"
EOF
  chmod +x "$TMPDIR/df"

  export MOCK_USAGE="$mock_usage"
  # Prepend mock directory to PATH so our script picks up the mock df
  PATH="$TMPDIR:$PATH"

  # Run the utility (capture both stdout and stderr)
  output=$("$UTIL_SCRIPT" -t "$threshold" /mock 2>&1) || true

  if [[ "$expect_warn" == "yes" ]]; then
    if [[ "$output" == *"Disk Guardian warns"* ]]; then
      echo "PASS $name"
    else
      echo "FAIL $name: expected warning, got:"
      echo "$output"
      exit 1
    fi
  else
    if [[ "$output" == *"All clear"* ]]; then
      echo "PASS $name"
    else
      echo "FAIL $name: expected all clear, got:"
      echo "$output"
      exit 1
    fi
  fi

  rm -rf "$TMPDIR"
}

# Test cases
run_test "below-threshold" "70" "80" "no"
run_test "above-threshold" "85" "80" "yes"

echo "All tests passed."
