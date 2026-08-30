#!/usr/bin/env bash
# Mock rationale: Run terraform init and validate locally without contacting AWS.
set -e

# Ensure terraform is available
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform not installed; skipping test."
  exit 0
fi

# Initialize the module with a temporary backend configuration
terraform init -backend=false >/dev/null

# Validate the configuration
terraform validate

echo "All Terraform checks passed."
