#!/usr/bin/env bash
set -euo pipefail

# Create temporary env files
old=$(mktemp)
new=$(mktemp)

cat > "$old" <<'EOF'
# Sample old env
DB_HOST=localhost
DB_PORT=5432
DEBUG=true
API_KEY=oldkey
EOF

cat > "$new" <<'EOF'
# Sample new env
DB_HOST=localhost
DB_PORT=5433
DEBUG=false
NEW_VAR=hello
API_KEY=oldkey
EOF

# Run the utility (relative path from tests directory)
output=$(bash ../src/env_diff.sh "$old" "$new")

# Expected fragments
expected_added="Added: NEW_VAR"
expected_changed="Changed: DB_PORT (5432->5433) DEBUG (true->false)"

# Verify added section exists
if [[ "$output" != *"$expected_added"* ]]; then
  echo "Test failed: missing added variables"
  echo "Output was:"
  echo "$output"
  exit 1
fi

# Verify changed section exists
if [[ "$output" != *"$expected_changed"* ]]; then
  echo "Test failed: missing changed variables"
  echo "Output was:"
  echo "$output"
  exit 1
fi

# Verify no removed section is printed
if [[ "$output" == *"Removed:"* ]]; then
  echo "Test failed: unexpected removed variables"
  echo "$output"
  exit 1
fi

echo "All tests passed"
