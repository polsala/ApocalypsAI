#!/usr/bin/env bash
set -e

# Initialize the module without a backend (local only)
terraform init -backend=false > /dev/null

# Validate syntax and configuration
terraform validate

# Perform a dry‑run plan with deterministic variable values
terraform plan -var 'portal_name=Test Portal' -var 'greeting=Hello, traveler!' -out=plan.out > /dev/null

echo "Terraform module validation passed"
exit 0
