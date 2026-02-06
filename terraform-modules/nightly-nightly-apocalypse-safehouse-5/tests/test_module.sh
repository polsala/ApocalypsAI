#!/usr/bin/env bash
set -e

# Move to the module root (one directory up from this script)
cd "$(dirname "$0")/.."

# Initialize Terraform without a backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

# Perform a dry‑run plan with example variables
terraform plan -input=false -var='bucket_name=test-safehouse' -out=plan.out > /dev/null

# If we reached this point, all checks passed
echo "All Terraform checks passed successfully."
