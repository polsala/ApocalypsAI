#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy AWS provider to validate configuration without real AWS calls.
# Initialize Terraform with a dummy backend.
terraform init -backend=false > /dev/null

# Validate the configuration.
terraform validate

# Generate a plan with -input=false and -refresh=false to avoid external calls.
terraform plan -input=false -refresh=false -out=plan.out > /dev/null

# Extract bucket name from the plan using terraform show -json.
# jq is used for JSON parsing; it is assumed to be available in the test environment.
bucket_name=$(terraform show -json plan.out | jq -r '.planned_values.root_module.resources[] | select(.type=="aws_s3_bucket") | .values.bucket')

if [[ -z "$bucket_name" ]]; then
  echo "Test failed: bucket not found in plan"
  exit 1
fi

# Ensure versioning is enabled in the plan.
versioning=$(terraform show -json plan.out | jq -r '.planned_values.root_module.resources[] | select(.type=="aws_s3_bucket") | .values.versioning.enabled')
if [[ "$versioning" != "true" ]]; then
  echo "Test failed: versioning not enabled"
  exit 1
fi

echo "All tests passed."
