#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: offline deterministic test using default variable values.

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Apply to generate manifest
terraform apply -auto-approve > /dev/null

# Verify file exists
MANIFEST_PATH=$(terraform output -raw manifest_path)
if [[ ! -f "$MANIFEST_PATH" ]]; then
  echo "Manifest file not created"
  exit 1
fi

# Simple content check against expected default JSON (order may vary, so we sort keys)
EXPECTED='{"water":10,"canned_food":20,"first_aid_kit":1,"flashlight":2}'
ACTUAL=$(cat "$MANIFEST_PATH" | tr -d ' \n')
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "Content mismatch"
  echo "Expected: $EXPECTED"
  echo "Actual:   $ACTUAL"
  exit 1
fi

echo "All tests passed"
