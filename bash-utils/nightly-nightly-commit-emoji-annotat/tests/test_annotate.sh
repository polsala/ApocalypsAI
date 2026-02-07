#!/usr/bin/env bash
set -e

# Mock input containing various commit types
input="feat: add new login\nfix: correct typo\ndocs update readme\nunknown change"

# Expected output with emojis
expected="✨ feat: add new login\n🛠️ fix: correct typo\n📚 docs update readme\n🔹 unknown change"

# Run the script with the mock input
output=$(printf "%b" "$input" | ./src/annotate.sh)

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
