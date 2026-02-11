#!/usr/bin/env bash

# test_annotate.sh – verifies that annotate.sh prefixes lines with correct emojis.
# This test runs offline by setting GIT_LOG_MOCK.

set -e

# Load the script under test
SCRIPT_PATH="../src/annotate.sh"

# Define a mocked git log (hash and message pairs)
export GIT_LOG_MOCK=$'a1b2c3 feat: add login\n'\
$'d4e5f6 fix: correct typo\n'\
$'7g8h9i docs: update README\n'\
$'j0k1l2 refactor: simplify loop\n'\
$'m3n4o5 test: add unit tests\n'\
$'p6q7r8 chore: clean build files\n'\
$'s9t0u1 other: miscellaneous change'

# Expected output
read -r -d '' EXPECTED <<'EOF'
a1b2c3 ✨ feat: add login
d4e5f6 🐛 fix: correct typo
7g8h9i 📚 docs: update README
j0k1l2 🔧 refactor: simplify loop
m3n4o5 ✅ test: add unit tests
p6q7r8 🧹 chore: clean build files
s9t0u1 🔖 other: miscellaneous change
EOF

# Run the script and capture output
OUTPUT=$(bash "$SCRIPT_PATH")

# Compare output to expected
if diff <(echo "$OUTPUT") <(echo "$EXPECTED"); then
    echo "All tests passed."
    exit 0
else
    echo "Test failed. Output differed from expected."
    echo "--- Output ---"
    echo "$OUTPUT"
    echo "--- Expected ---"
    echo "$EXPECTED"
    exit 1
fi
