#!/usr/bin/env bash

# nightly-disk-guardian tests
# These tests run without touching the real filesystem by mocking df output via the DF_MOCK env var.

set -euo pipefail

# Helper to run the script and capture output
run_script() {
  local path="$1"
  local threshold="$2"
  local df_mock="$3"
  DF_MOCK="$df_mock" ./src/main.sh -p "$path" -t "$threshold"
}

# Test case 1: usage below threshold – expect no output
mock_df_below="Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda1 1000000 400000 600000 40% $PATH_TO_CHECK"
output=$(run_script "/" 80 "$mock_df_below" || true)
if [[ -n "$output" ]]; then
  echo "FAIL: Expected no warning when usage is below threshold, got: $output"
  exit 1
fi

echo "PASS: No warning when usage below threshold"

# Test case 2: usage above threshold – expect warning containing path and percentage
mock_df_above="Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda1 1000000 850000 150000 85% /home"
output=$(run_script "/home" 80 "$mock_df_above")
if [[ "$output" != *"Warning! Your /home is 85% full"* ]]; then
  echo "FAIL: Expected warning for high usage, got: $output"
  exit 1
fi

echo "PASS: Warning emitted when usage exceeds threshold"

# Test case 3: custom message file
cat > /tmp/messages.txt <<'EOF'
Your disk is a black hole!
Time to Marie Kondo your files.
EOF
mock_df_custom="Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda1 1000000 900000 100000 90% /data"
output=$(DF_MOCK="$mock_df_custom" ./src/main.sh -p "/data" -t 80 -m /tmp/messages.txt)
if [[ "$output" != *"Your disk is a black hole!"* && "$output" != *"Time to Marie Kondo your files."* ]]; then
  echo "FAIL: Expected one of the custom messages, got: $output"
  exit 1
fi

echo "PASS: Custom message file is used when provided"

# Cleanup
rm -f /tmp/messages.txt

exit 0
