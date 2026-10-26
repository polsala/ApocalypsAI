#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without backend or provider download
terraform init -backend=false -get=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan
terraform plan -input=false -out=plan.out > /dev/null

# Ensure the null_resource is present in the plan
if ! terraform show -json plan.out | grep -q '"type":"null_resource"'; then
  echo "Test failed: null_resource.safehouse_bucket not found in plan"
  exit 1
fi

echo "All tests passed."
