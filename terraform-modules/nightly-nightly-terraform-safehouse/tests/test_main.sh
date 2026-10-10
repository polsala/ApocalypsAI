#!/usr/bin/env bash
set -e

# Mock rationale: this script runs Terraform commands locally without contacting AWS.
# It uses the "-backend=false" flag to avoid remote state and dummy variables.

# Initialize Terraform (no backend)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Generate a plan with static variables; no actual AWS calls are made because no provider credentials are required for validation only.
terraform plan -input=false -var="aws_region=us-east-1" -out=plan.out > /dev/null

echo "All Terraform checks passed."
