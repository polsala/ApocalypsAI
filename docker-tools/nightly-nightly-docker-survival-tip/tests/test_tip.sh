#!/usr/bin/env bash
# Tests for tip.sh
# Mock rationale: we invoke tip.sh with a known index and verify output.

set -e

# Path to the script under test
SCRIPT="../src/tip.sh"

# Expected tips (must match the array in tip.sh)
expected=(
"Always carry a spare bottle of water."
"Never trust a smiling mutant."
"Keep your flashlight charged."
"Remember: sand is your friend."
"Stay low, stay quiet."
)

# Test each index
for i in "${!expected[@]}"; do
  output=$($SCRIPT $i)
  if [[ "$output" != "${expected[$i]}" ]]; then
    echo "Test failed for index $i: expected '${expected[$i]}', got '$output'"
    exit 1
  fi
done

echo "All tests passed."
