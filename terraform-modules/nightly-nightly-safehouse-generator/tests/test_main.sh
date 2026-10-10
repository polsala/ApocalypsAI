#!/usr/bin/env bash
set -e

# Initialize Terraform without downloading any providers (null is built‑in)
terraform init -backend=false -get=false > /dev/null

# Apply the module with a custom message to ensure variable handling works
terraform apply -auto-approve -input=false -var='welcome_message=TestMessage' > /dev/null

# Path to the generated message file
FILE="$(pwd)/safehouse/message.txt"

# Verify the file exists
if [[ ! -f "$FILE" ]]; then
  echo "FAIL: message file not found at $FILE"
  exit 1
fi

# Verify the file content matches the supplied variable
CONTENT=$(cat "$FILE")
if [[ "$CONTENT" != "TestMessage" ]]; then
  echo "FAIL: unexpected file content: $CONTENT"
  exit 1
fi

echo "PASS"
exit 0
