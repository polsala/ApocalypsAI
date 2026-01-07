#!/usr/bin/env bash
set -euo pipefail

# Change to the directory containing the module
cd "$(dirname "$0")/.."

# Initialize Terraform with a local backend (no remote state)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a quick plan with mock variables to ensure no errors
terraform plan \
  -var "bucket_name=test-bucket-$(date +%s)" \
  -var "password_length=16" \
  -out=plan.out > /dev/null

# If we reached this point, the module passed basic checks
echo "✅ Terraform module validation succeeded"

# Mock rationale: The test does not contact AWS because the provider is configured with default (no credentials) and the backend is disabled. Terraform will still perform static checks.
