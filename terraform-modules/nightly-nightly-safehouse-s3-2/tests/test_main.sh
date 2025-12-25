#!/usr/bin/env bash
set -e

# Initialize Terraform (backend disabled for test isolation)
terraform init -backend=false > /dev/null

# Validate the configuration – should exit with status 0
terraform validate

# Run a plan with a sample bucket name and capture output
PLAN_OUTPUT=$(terraform plan -var 'bucket_name=test-safehouse-bucket' -no-color)

# Verify that the plan includes the aws_s3_bucket resource
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.safehouse'

echo "All tests passed."
