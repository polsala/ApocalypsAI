#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without a remote backend
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Generate a plan (offline, no credentials needed)
terraform plan -input=false -out=plan.out > plan.txt

# Verify that the plan includes the expected S3 bucket resource
if grep -q "aws_s3_bucket.safehouse" plan.txt; then
  echo "Test passed: S3 bucket resource found in plan."
  exit 0
else
  echo "Test failed: S3 bucket resource not found."
  exit 1
fi
