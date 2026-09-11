#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and plan locally, then checks that the plan includes the local_file resource.
set -e

# Ensure a clean working directory
rm -rf .terraform .terraform.lock.hcl

# Initialize Terraform without a backend (offline safe)
terraform init -backend=false > /dev/null

# Generate a plan and capture output
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>&1)

# Verify that the plan contains the local_file resource
if echo "$PLAN_OUTPUT" | grep -q "local_file.bucket_config"; then
  echo "PASS: local_file.bucket_config is present in the plan"
  exit 0
else
  echo "FAIL: Expected local_file.bucket_config not found in the plan"
  exit 1
fi
