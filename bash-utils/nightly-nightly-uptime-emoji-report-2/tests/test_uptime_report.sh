#!/usr/bin/env bash
set -euo pipefail

# Helper to run the script with a mocked uptime file.
run_script() {
  local mock_path="$1"
  UPTIME_FILE="$mock_path" ./src/uptime_report.sh
}

# Expected output mapping for various uptime values (seconds).
declare -A cases
cases["0"]="Uptime: 0 days 🌱"
cases["43200"]="Uptime: 0 days 🌱"   # 12 hours
cases["90000"]="Uptime: 1 days 🌿"   # 25 hours
cases["604800"]="Uptime: 7 days 🌳"  # exactly 7 days (>=7 triggers tree)
cases["1209600"]="Uptime: 14 days 🌳"

passed=0
total=0

for seconds in "${!cases[@]}"; do
  ((total++))
  mock_file=$(mktemp)
  # /proc/uptime format: "seconds idle_seconds"
  echo "$seconds 0.00" > "$mock_file"
  output=$(run_script "$mock_file")
  rm -f "$mock_file"
  expected="${cases[$seconds]}"
  if [[ "$output" == "$expected" ]]; then
    ((passed++))
  else
    echo "FAIL for $seconds seconds: expected '$expected', got '$output'"
  fi
done

echo "$passed/$total tests passed"
exit 0
