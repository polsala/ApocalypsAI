#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a temporary directory to init the module with dummy variables.
TMPDIR=$(mktemp -d)
cp -r . "$TMPDIR/module"
cd "$TMPDIR/module"

# Initialize Terraform without a backend (offline test)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a plan with placeholder variable values (no real AWS access required)
terraform plan -input=false \
  -var 'bucket_name=test-safehouse-bucket' \
  -var 'ssm_parameter_name=/test/apocalypse/password' \
  -out=plan.out > /dev/null

echo "Terraform module validation and plan succeeded."
