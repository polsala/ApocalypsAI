#!/usr/bin/env bash
set -e

# Ensure we are in the module directory
cd "$(dirname "$0")/.."

# Initialize Terraform (no backend to keep it offline)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan without prompting for input
terraform plan -input=false -out=plan.out > /dev/null

# Verify that the expected null_resource is present in the plan
if ! grep -q "null_resource.safehouse" plan.out; then
  echo "ERROR: Expected null_resource.safehouse not found in plan"
  exit 1
fi

# Clean up generated files
rm -f plan.out .terraform.lock.hcl .terraform/ .mock_safehouse.txt

echo "All tests passed"
