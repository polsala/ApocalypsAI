#!/usr/bin/env bash
set -e

# Initialize Terraform without remote backend (offline safe)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan and capture output
plan_output=$(terraform plan -no-color -input=false)

# Check that the plan includes the expected S3 bucket resource
if echo "$plan_output" | grep -q "aws_s3_bucket.safehouse"; then
  echo "Test passed: bucket resource found in plan."
else
  echo "Test failed: bucket resource not found."
  exit 1
fi
