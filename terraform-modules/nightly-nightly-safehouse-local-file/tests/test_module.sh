#!/usr/bin/env bash
set -e

# Ensure we are in the module directory
cd "$(dirname "$0")/.."

# Initialize Terraform (no backend, no remote plugins needed)
terraform init -backend=false > /dev/null 2>&1

# Validate the configuration syntax
terraform validate

# Perform a dry‑run plan (no apply)
terraform plan -input=false -out=plan.out > /dev/null 2>&1

echo "Tests passed"

# Cleanup temporary files
rm -rf .terraform .terraform.lock.hcl plan.out
