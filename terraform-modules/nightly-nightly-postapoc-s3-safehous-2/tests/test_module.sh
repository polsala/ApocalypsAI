#!/usr/bin/env bash
set -e

# Mock rationale: Use dummy AWS credentials to avoid real calls
export AWS_ACCESS_KEY_ID="dummy"
export AWS_SECRET_ACCESS_KEY="dummy"
export AWS_DEFAULT_REGION="us-east-1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan with test variables
terraform plan -var="bucket_name=apocalypse-safehouse-test" -out=plan.out > plan.txt

# Ensure the plan contains the S3 bucket resource
if ! grep -q "aws_s3_bucket.safehouse" plan.txt; then
  echo "Test failed: S3 bucket resource not found in plan."
  exit 1
fi

echo "All tests passed."
