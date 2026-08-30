#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy AWS provider to validate config without real AWS calls.
# Terraform will only validate syntax and provider schema.

# Initialize Terraform with a temporary backend (no remote state)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a plan with mock variable values; the plan will succeed as long as the config is valid.
terraform plan -input=false -no-color -out=plan.out -var="bucket_name=test-safehouse-$(date +%s)" > /dev/null

echo "✅ Terraform module validation passed."
