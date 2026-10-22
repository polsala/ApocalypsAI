#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy provider configuration to avoid real AWS calls.
# Initialize Terraform without remote backend.
terraform init -backend=false > /dev/null

# Validate configuration.
terraform validate

# Generate a plan with dummy provider credentials (using environment variables that are ignored).
export AWS_ACCESS_KEY_ID="mock"
export AWS_SECRET_ACCESS_KEY="mock"
export AWS_DEFAULT_REGION="us-east-1"

PLAN_OUTPUT=$(terraform plan -input=false -no-color -out=plan.out 2>&1)

# Check that plan contains the S3 bucket resource.
if echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.safehouse'; then
  echo "Test passed: S3 bucket resource is present in plan."
else
  echo "Test failed: S3 bucket resource not found in plan."
  exit 1
fi

# Clean up
rm -f plan.out
