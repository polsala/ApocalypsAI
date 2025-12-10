#!/usr/bin/env bash
set -euo pipefail

# Mock df command to provide deterministic output
DF_CMD() {
  cat <<'EOF'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   10G   40G  20% /
/dev/sda2       100G   85G   15G  85% /data
EOF
}
export -f DF_CMD

# Run the utility (path argument is ignored because DF_CMD does not use it)
output=$(bash ../../src/main.sh /)

expected=$(cat <<'EOF'
/dev/sda1        50G   10G   40G  20% / 🟢
/dev/sda2       100G   85G   15G  85% /data 💀
EOF
)

if [ "$output" = "$expected" ]; then
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
