#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy variables to validate configuration without external calls.
# Initialize Terraform without remote backend.
terraform init -backend=false > /dev/null

# Validate the configuration.
terraform validate

# Run a plan with dummy values to ensure resources can be planned.
terraform plan -input=false -no-color -var "bucket_name=test-bucket-$(date +%s)" > /dev/null

echo "All Terraform checks passed."
