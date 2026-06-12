#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend (offline safe)
terraform -chdir=src init -backend=false > /dev/null

# Validate the configuration syntax
terraform -chdir=src validate

# Generate a plan (no‑color for easier parsing)
PLAN_OUTPUT=$(terraform -chdir=src plan -no-color -input=false)

# Ensure the plan includes the expected S3 bucket resource
if echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.safehouse'; then
  echo "Test passed: S3 bucket resource found in plan."
else
  echo "Test failed: S3 bucket resource not found."
  exit 1
fi
