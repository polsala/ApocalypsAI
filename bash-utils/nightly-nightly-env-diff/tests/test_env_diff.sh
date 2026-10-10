#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create temporary .env files for deterministic testing
old=$(mktemp)
new=$(mktemp)

cat > "$old" <<'EOF'
FOO=1
BAR=2
BAZ=old
# COMMENT line
EOF

cat > "$new" <<'EOF'
FOO=1
BAR=3
NEWVAR=hello
BAZ=old
EOF

expected=$(cat <<'EXPECTED'
Added:
  NEWVAR

Changed:
  BAR

Unchanged:
  FOO
  BAZ
EXPECTED
)

output=$(bash ../src/env_diff.sh "$old" "$new")

if [[ "$output" != "$expected" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi

echo "All tests passed"
