#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create temporary .env files with known contents
tmpdir=$(mktemp -d)
old_file="$tmpdir/old.env"
new_file="$tmpdir/new.env"

cat > "$old_file" <<'EOF'
# Sample old env
DB_HOST=localhost
DB_PORT=5432
API_KEY=oldkey
DEBUG=false
EOF

cat > "$new_file" <<'EOF'
# Sample new env
DB_HOST=localhost
DB_PORT=5433
API_KEY=newkey
NEW_VAR=hello
EOF

# Run the utility
output=$(bash ../../src/diff_env.sh "$old_file" "$new_file")

# Expected output
expected=$(cat <<'EOT'
Added variables:
NEW_VAR

Removed variables:
DEBUG

Changed variables:
DB_PORT: 5432 => 5433
API_KEY: oldkey => newkey
EOT
)

# Compare actual vs expected
if [[ "$output" != "$expected" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi

echo "All tests passed"
