#!/usr/bin/env bash
# Simple test harness for nightly-radiation-disk-monitor
# No external test framework required; runs in pure Bash.

set -e

# Helper: run the monitor with a mocked df output line
run_monitor() {
  local df_line="$1"
  # Create a temporary mock df script
  local mock_df=$(mktemp)
  chmod +x "$mock_df"
  cat <<'EOF' > "$mock_df"
#!/usr/bin/env bash
# Mock df: prints header then the injected line
echo "Filesystem Size Used Avail Use% Mounted on"
echo "$DF_LINE"
EOF
  # Export the line for the mock script
  DF_LINE="$df_line" DF_CMD="$mock_df" ./src/monitor.sh
  local status=$?
  rm -f "$mock_df"
  return $status
}

# Test case: Safe level (20% usage)
output=$(run_monitor "devtmpfs 1024 200 824 20% /dev")
if [[ "$output" != *"Safe"* ]]; then
  echo "FAIL: Expected Safe level, got: $output"
  exit 1
fi

# Test case: Elevated level (80% usage)
output=$(run_monitor "devtmpfs 1024 800 224 80% /dev")
if [[ "$output" != *"Elevated"* ]]; then
  echo "FAIL: Expected Elevated level, got: $output"
  exit 1
fi

# Test case: Critical level (95% usage)
output=$(run_monitor "devtmpfs 1024 975 49 95% /dev")
if [[ "$output" != *"Critical"* ]]; then
  echo "FAIL: Expected Critical level, got: $output"
  exit 1
fi

echo "All tests passed"
