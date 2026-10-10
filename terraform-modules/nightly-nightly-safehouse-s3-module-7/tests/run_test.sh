#!/usr/bin/env bash
set -e

# Initialize Terraform without remote backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a plan with mock variables; no real AWS credentials are needed
terraform plan -input=false -var="bucket_name=test-safehouse-bucket" -var="region=us-east-1" -out=plan.out > /dev/null

# Ensure the generated plan contains the expected S3 bucket resource
# Mock rationale: we inspect the JSON plan output for the resource type without contacting AWS.
if ! terraform show -json plan.out | grep -q '"type":"aws_s3_bucket"'; then
  echo "Test failed: S3 bucket not found in plan"
  exit 1
fi

echo "All tests passed."
