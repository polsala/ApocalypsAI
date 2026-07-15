#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan (no‑op) and capture output
plan_output=$(terraform plan -no-color -input=false 2>/dev/null || true)

# Check that versioning is set to enabled in the plan
if echo "$plan_output" | grep -q "versioning.*enabled = true"; then
  echo "PASS: Versioning is enabled"
else
  echo "FAIL: Versioning not found"
  exit 1
fi

echo "All checks passed."
