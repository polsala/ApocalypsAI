#!/usr/bin/env bash
set -e

# Initialize Terraform (offline, no backend)
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan and capture output
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>&1)

# Check that the lifecycle rule is present
if echo "$PLAN_OUTPUT" | grep -q "expire-old-scrap"; then
  echo "Test passed: lifecycle rule detected."
  exit 0
else
  echo "Test failed: lifecycle rule not found."
  exit 1
fi
