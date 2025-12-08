#!/usr/bin/env bash

# Mock rationale: This test checks that the Dockerfile contains the expected COPY and ENTRYPOINT directives,
# and that the entrypoint script includes the emoji mapping logic. It runs purely on the filesystem, so it is
# deterministic and offline.

set -e

# Determine repository root (assumes this script is run from the utility root)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.. && pwd)"

# Load file contents
DOCKERFILE="$ROOT_DIR/Dockerfile"
ENTRYPOINT="$ROOT_DIR/src/entrypoint.sh"

# Test 1: Dockerfile must use alpine base image
if ! grep -q "FROM alpine" "$DOCKERFILE"; then
  echo "❌ Dockerfile does not contain 'FROM alpine'"
  exit 1
fi

# Test 2: Dockerfile must copy entrypoint.sh
if ! grep -q "COPY src/entrypoint.sh /entrypoint.sh" "$DOCKERFILE"; then
  echo "❌ Dockerfile missing correct COPY directive"
  exit 1
fi

# Test 3: Dockerfile must set ENTRYPOINT correctly
if ! grep -q "ENTRYPOINT \[\"/entrypoint.sh\"\]" "$DOCKERFILE"; then
  echo "❌ Dockerfile missing correct ENTRYPOINT"
  exit 1
fi

# Test 4: entrypoint.sh must be executable (shebang present)
if ! head -n1 "$ENTRYPOINT" | grep -q "#!/usr/bin/env bash"; then
  echo "❌ entrypoint.sh missing shebang"
  exit 1
fi

# Test 5: entrypoint.sh must contain the emoji mapping function
if ! grep -q "map_emoji" "$ENTRYPOINT"; then
  echo "❌ entrypoint.sh missing map_emoji function"
  exit 1
fi

# Test 6: Verify that each log level maps to the correct emoji (using the function directly)
# We'll source the script in a subshell to access the function.
source "$ENTRYPOINT"

# Helper to capture function output
emoji_for() {
  map_emoji "$1"
}

if [[ "$(emoji_for INFO)" != "ℹ️" ]]; then echo "❌ INFO mapping failed"; exit 1; fi
if [[ "$(emoji_for WARN)" != "⚠️" ]]; then echo "❌ WARN mapping failed"; exit 1; fi
if [[ "$(emoji_for ERROR)" != "❌" ]]; then echo "❌ ERROR mapping failed"; exit 1; fi
if [[ "$(emoji_for DEBUG)" != "🐞" ]]; then echo "❌ DEFAULT mapping failed"; exit 1; fi

echo "✅ All tests passed"
