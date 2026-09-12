#!/usr/bin/env bash
set -e

# Initialize Terraform without remote backend
terraform init -backend=false -input=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan
terraform plan -out=plan.out -input=false > /dev/null

# Ensure the plan contains the S3 bucket resource
if ! terraform show -json plan.out | grep -q '"type":"aws_s3_bucket"'; then
  echo "Test failed: S3 bucket resource not found in plan."
  exit 1
fi

echo "All tests passed."
