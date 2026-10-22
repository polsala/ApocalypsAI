#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Generate a plan with a fixed bucket name prefix
PLAN_OUTPUT=$(terraform plan -input=false -var 'bucket_name_prefix=testbucket' -no-color)

# Ensure the plan contains the expected aws_s3_bucket resource
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.this'

echo "Test passed: S3 bucket resource is present in plan."
