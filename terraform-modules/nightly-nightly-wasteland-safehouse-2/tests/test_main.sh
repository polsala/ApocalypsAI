#!/usr/bin/env bash
set -euo pipefail

# Initialize the module without a remote backend
terraform -chdir=src init -backend=false > /dev/null

# Validate the configuration syntax
terraform -chdir=src validate

# Run a plan with example variables (no actual apply)
terraform -chdir=src plan -var 'bucket_name=test-safehouse-bucket' -var 'radiation_level=low' -out=plan.out > /dev/null

echo "All Terraform checks passed."
