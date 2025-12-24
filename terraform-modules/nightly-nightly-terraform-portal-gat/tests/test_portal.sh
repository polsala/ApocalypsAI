#!/usr/bin/env bash
set -e

# Initialize Terraform without a backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Generate a plan and capture its output
PLAN_OUTPUT=$(terraform plan -no-color -input=false)

# Ensure the null_resource.portal is present in the plan
if echo "$PLAN_OUTPUT" | grep -q "null_resource.portal"; then
  echo "Test passed: portal resource present."
else
  echo "Test failed: portal resource missing."
  exit 1
fi
