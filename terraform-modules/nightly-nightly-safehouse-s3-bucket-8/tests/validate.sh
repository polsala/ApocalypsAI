#!/usr/bin/env bash
set -e

# Initialize Terraform (no backend to keep it local)
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan without refreshing state (offline)
terraform plan -refresh=false -out=plan.out > /dev/null

# Mock rationale: offline test using -refresh=false ensures no external calls.

echo "All checks passed."
