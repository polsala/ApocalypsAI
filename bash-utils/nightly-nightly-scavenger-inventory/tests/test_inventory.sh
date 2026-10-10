#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Provide deterministic input and compare expected output.

INPUT=$(cat <<'EOF'
water 2 5
canned_food 1 10
medkit 0.5 2
EOF
)

EXPECTED=$(cat <<'EOF'
Scavenger Inventory:
- water x5 (2 each) = 10.00
- canned_food x10 (1 each) = 10.00
- medkit x2 (0.5 each) = 1.00
Total weight: 21.00 units
Survival rating: Sturdy
EOF
)

# Run the script with the deterministic input
OUTPUT=$(printf "%s\n" "$INPUT" | bash src/inventory.sh)

if diff <(printf "%s\n" "$OUTPUT") <(printf "%s\n" "$EXPECTED"); then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Expected:"
  echo "$EXPECTED"
  echo "Got:"
  echo "$OUTPUT"
  exit 1
fi
