#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy credentials to avoid real AWS calls.
export AWS_ACCESS_KEY_ID="mock"
export AWS_SECRET_ACCESS_KEY="mock"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan without contacting AWS (refresh disabled)
terraform plan -input=false -refresh=false -out=plan.out > /dev/null

echo "All tests passed."
