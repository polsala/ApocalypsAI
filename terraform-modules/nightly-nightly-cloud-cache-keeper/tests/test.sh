#!/bin/bash
set -euo pipefail

echo "Running Nightly Cloud Cache Keeper Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (without backend to keep it offline and deterministic)
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan the Terraform configuration
# We expect a successful plan, which means exit code 0 (no changes, if resources exist) or 2 (changes to apply).
# For a fresh plan, it will typically be 2.
echo "Planning Terraform configuration..."
terraform plan -detailed-exitcode -out=tfplan

PLAN_EXIT_CODE=$?

# Mock rationale: Terraform plan requires a provider configuration, but for offline testing,
# we only care that the module can be successfully planned without syntax or configuration errors.
# We use mock AWS credentials in tests/main.tf to satisfy the provider requirement without
# needing actual cloud access. The -detailed-exitcode allows us to check for successful planning.
# An exit code of 0 means no changes, 2 means changes are pending. Both are considered successful for validation.
if [[ "$PLAN_EXIT_CODE" -eq 0 || "$PLAN_EXIT_CODE" -eq 2 ]]; then
  echo "Terraform plan successful (exit code: $PLAN_EXIT_CODE)."
  rm tfplan # Clean up the plan file
  echo "All tests passed!"
  exit 0
else
  echo "Terraform plan failed with exit code: $PLAN_EXIT_CODE."
  rm -f tfplan # Clean up if it exists
  exit 1
fi
