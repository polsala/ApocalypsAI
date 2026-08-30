#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create temporary .env files with known content
TMPDIR=$(mktemp -d)
OLD_ENV="$TMPDIR/old.env"
NEW_ENV="$TMPDIR/new.env"

cat >"$OLD_ENV" <<'EOF'
# Old environment
VAR1=foo
VAR2=bar
EOF

cat >"$NEW_ENV" <<'EOF'
# New environment
VAR2=baz
VAR3=qux
EOF

# Execute the utility
OUTPUT=$(bash ../src/diff_env.sh "$OLD_ENV" "$NEW_ENV")

# Expected deterministic output
EXPECTED=$'🚀 Added variables:\n  + VAR3=qux\n🗑️ Removed variables:\n  - VAR1=foo\n🔄 Changed variables:\n  * VAR2: "bar" → "baz"'

if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$EXPECTED"
  echo "Got:"
  echo "$OUTPUT"
  exit 1
fi

echo "All tests passed"
