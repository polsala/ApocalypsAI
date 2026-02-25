#!/usr/bin/env bash

# Test for nightly-env-var-diff
# This test creates two temporary .env files, runs the diff script, and verifies the output.

set -euo pipefail

# Create a temporary directory for test fixtures
TMPDIR=$(mktemp -d)

# Mock rationale: create deterministic old.env content
cat > "$TMPDIR/old.env" <<'EOF'
# Old environment
DB_HOST=localhost
DB_PORT=5432
API_KEY=oldkey
EOF

# Mock rationale: create deterministic new.env content
cat > "$TMPDIR/new.env" <<'EOF'
# New environment
DB_HOST=localhost
DB_PORT=5433
API_KEY=newkey
NEW_VAR=hello
EOF

# Expected output (exact string, sections only when they have entries)
read -r -d '' EXPECTED <<'EOT'
Added:
NEW_VAR=hello

Modified:
DB_PORT: 5432 -> 5433
API_KEY: oldkey -> newkey

EOT

# Run the utility
OUTPUT=$(bash ../../src/diff_env.sh "$TMPDIR/old.env" "$TMPDIR/new.env")

# Compare output to expected
if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test failed"
  echo "--- Expected ---"
  echo "$EXPECTED"
  echo "--- Got ---"
  echo "$OUTPUT"
  exit 1
fi

echo "All tests passed"
