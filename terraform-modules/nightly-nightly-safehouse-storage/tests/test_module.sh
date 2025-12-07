#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Apply with auto-approve (creates the safehouse directory locally)
terraform apply -auto-approve -input=false > /dev/null

# Capture outputs
SAFEHOUSE_PATH=$(terraform output -raw safehouse_path)

# Verify the directory exists
if [[ ! -d "$SAFEHOUSE_PATH" ]]; then
  echo "FAIL: Safehouse directory not created"
  exit 1
fi

# Verify version.txt exists and contains the expected version
if [[ ! -f "$SAFEHOUSE_PATH/version.txt" ]]; then
  echo "FAIL: version.txt not found"
  exit 1
fi

EXPECTED_VERSION="1"
ACTUAL_VERSION=$(cat "$SAFEHOUSE_PATH/version.txt")
if [[ "$ACTUAL_VERSION" != "$EXPECTED_VERSION" ]]; then
  echo "FAIL: version mismatch (expected $EXPECTED_VERSION, got $ACTUAL_VERSION)"
  exit 1
fi

echo "PASS: Safehouse storage module works as expected"

# Cleanup resources
terraform destroy -auto-approve -input=false > /dev/null
