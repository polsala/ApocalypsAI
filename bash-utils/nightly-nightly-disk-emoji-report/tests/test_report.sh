#!/usr/bin/env bash
set -euo pipefail

# Mock df data
cat > /tmp/mock_df.txt <<'EOF'
/dev/sda1 30%
/dev/sda2 85%
tmpfs 5%
EOF

expected=$(cat <<'EOT'
/dev/sda1 🟥🟥🟥🟩🟩🟩🟩🟩🟩🟩 (30%)
/dev/sda2 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟩 (85%)
tmpfs 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 (5%)
EOT
)

output=$(bash "$(dirname "$0")/../src/report.sh" /tmp/mock_df.txt)

if diff <(echo "$output") <(echo "$expected"); then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Got:"
  echo "$output"
  echo "Expected:"
  echo "$expected"
  exit 1
fi
