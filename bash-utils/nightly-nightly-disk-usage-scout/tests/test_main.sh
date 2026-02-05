#!/usr/bin/env bash
set -euo pipefail

# Mock du command that emits predictable size data
mock_du() {
  cat <<'EOF'
4096 ./dirA
2048 ./dirB
1024 ./dirC
512 ./dirD
EOF
}
export DU_CMD=mock_du

# Execute the utility (script is located one directory up)
output=$(../src/main.sh -n 2 .)

expected="4096 ./dirA\n2048 ./dirB"

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Expected:"
  echo -e "$expected"
  echo "Got:"
  echo -e "$output"
  exit 1
fi
