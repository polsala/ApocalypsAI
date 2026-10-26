#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy AWS provider to avoid real calls.
# Initialize Terraform with -backend=false to keep everything in-memory.
terraform init -backend=false > /dev/null

# Validate configuration syntax and provider requirements.
terraform validate

# Generate a plan with dummy variables; expect no errors.
terraform plan -input=false -var="bucket_name=test-safehouse-bucket" -var="enable_secret=false" -out=plan.out > /dev/null

echo "All tests passed."
