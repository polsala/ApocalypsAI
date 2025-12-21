#!/usr/bin/env bash
set -euo pipefail

SCRIPT="$(cd "$(dirname \"${BASH_SOURCE[0]}\")/../src" && pwd)/echo_echo.sh"

# Test deterministic output
export RANDOM=5
output=$("$SCRIPT")
expected="The sky is a canvas of possibility."
if [[ "$output" != "$expected" ]]; then
  echo "Expected '$expected', got '$output'"
  exit 1
fi

# Test --list outputs all phrases
list_output=$("$SCRIPT" --list)
for phrase in "The sky is a canvas of possibility." "Every bug is a hidden treasure." "Keep calm and code on." "When in doubt, add a comment." "The terminal is your playground."; do
  if ! grep -qF "$phrase" <<<"$list_output"; then
    echo "Phrase '$phrase' not found in list output"
    exit 1
  fi
done

# Test exit status
"$SCRIPT" >/dev/null
if [[ $? -ne 0 ]]; then
  echo "Script exited with non-zero status"
  exit 1
fi

echo "All tests passed"
