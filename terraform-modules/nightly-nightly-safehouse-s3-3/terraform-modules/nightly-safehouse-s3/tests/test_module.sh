#!/usr/bin/env bash
# Test script for nightly‑safehouse‑s3 Terraform module
# Mock rationale: we run Terraform in local mode without real AWS credentials.
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MODULE_DIR"

# Initialise Terraform with a dummy backend (local)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan with dummy variables (bucket name must be unique; we use a random suffix)
export TF_VAR_bucket_name="apocalypse-safehouse-$(date +%s)"
export TF_VAR_create_supply_file=true

terraform plan -input=false -out=plan.out > /dev/null

# Ensure the plan contains the expected resources
if ! terraform show -json plan.out | grep -q 'aws_s3_bucket.safehouse'; then
  echo "ERROR: S3 bucket resource not found in plan"
  exit 1
fi
if ! terraform show -json plan.out | grep -q 'aws_s3_object.supply_cache'; then
  echo "ERROR: supply‑cache object not found in plan"
  exit 1
fi

echo "All checks passed. Terraform module is valid."
