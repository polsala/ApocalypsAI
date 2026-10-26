#!/usr/bin/env bash

set -euo pipefail

# Create temporary .env files
old=$(mktemp)
new=$(mktemp)

cat > "$old" <<'EOF'
VAR1=foo
VAR2=bar
VAR3=baz
# comment line
EOF

cat > "$new" <<'EOF'
VAR1=foo
VAR2=qux
VAR4=quux
EOF

expected=$(cat <<'EOT'
Added:
VAR4=quux

Removed:
VAR3=baz

Modified:
VAR2: bar -> qux

EOT
)

# Run the utility (relative path from tests directory)
output=$(../src/env_diff.sh "$old" "$new")

if [[ "$output" == "$expected" ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
