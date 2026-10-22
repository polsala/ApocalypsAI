#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without remote backend (offline mode)
terraform init -backend=false -input=false > /dev/null

# Validate configuration syntax and internal consistency
terraform validate

# Generate a plan to ensure resources can be processed; discard output
terraform plan -input=false -out=plan.out > /dev/null

echo "All Terraform checks passed."
