#!/usr/bin/env bash
set -euo pipefail

SCRIPT="./src/commit-emoji.sh"

# Helper to test
test_case() {
  local input="$1"
  local expected="$2"
  local output
  output=$($SCRIPT <<< "$input")
  if [ "$output" != "$expected" ]; then
    echo "FAIL: input: $input"
    echo "Expected: $expected"
    echo "Got: $output"
    exit 1
  fi
}

# Test cases
test_case "feat: add new API endpoint" "🎉 feat: add new API endpoint"
test_case "fix: resolve crash on startup" "🐛 fix: resolve crash on startup"
test_case "docs: update README" "📚 docs: update README"
test_case "style: format code" "✨ style: format code"
test_case "refactor: improve performance" "🔧 refactor: improve performance"
test_case "test: add unit tests" "✅ test: add unit tests"
test_case "chore: bump version" "🔄 chore: bump version"
test_case "unknown: do something" "unknown: do something"

# Test write-back
TMPFILE=$(mktemp)
echo "feat: temporary commit" > "$TMPFILE"
$SCRIPT -w "$TMPFILE"
cat "$TMPFILE" | grep -q "^🎉 feat: temporary commit" || { echo "FAIL write-back"; exit 1; }
rm "$TMPFILE"

echo "All tests passed"
