#!/usr/bin/env bash
set -e

# Navigate to module root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Initialize Terraform without a backend (offline-friendly)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a plan with example variables (no actual AWS calls are made)
terraform plan \
  -var 'bucket_name=test-bucket-123' \
  -var 'index_document=index.html' \
  -var 'error_document=error.html' \
  -var 'enable_cloudfront=false' \
  -out=plan.out > /dev/null

# Ensure the plan contains the expected S3 bucket resource
if ! grep -q 'aws_s3_bucket.website' plan.out; then
  echo "Expected S3 bucket resource not found in plan"
  exit 1
fi

echo "All tests passed!"
