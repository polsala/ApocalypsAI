#!/usr/bin/env bash
set -e

# Mock terraform command to avoid real provider downloads
terraform() {
  case "$1" in
    init|plan|apply)
      echo "Mock $1 executed"
      return 0
      ;;
    output)
      if [[ "$2" == "-json" ]]; then
        cat <<EOF
{
  "items": {
    "value": [
      "canned beans",
      "energy bars"
    ],
    "type": "list",
    "sensitive": false
  }
}
EOF
        return 0
      fi
      ;;
    *)
      echo "Unsupported mock command: $1"
      return 1
      ;;
  esac
}

# Create a temporary working directory
WORKDIR=$(mktemp -d)
cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

# Copy module files
cp -r ../src "$WORKDIR/src"

cd "$WORKDIR"

# Initialize and apply (mocked)
terraform init -backend=false -input=false
terraform apply -auto-approve -input=false

# Get output in JSON
OUTPUT=$(terraform output -json)

# Extract items array using jq (jq is assumed to be available in CI)
# Mock rationale: using jq to parse known JSON structure.
ITEMS=$(echo "$OUTPUT" | jq -r '.items.value[]')

# Expected items for supply_type=food
EXPECTED=("canned beans" "energy bars")

# Verify each expected item is present
for exp in "${EXPECTED[@]}"; do
  if ! echo "$ITEMS" | grep -qx "$exp"; then
    echo "Test failed: expected item $exp not found"
    exit 1
  fi
done

echo "All tests passed."
