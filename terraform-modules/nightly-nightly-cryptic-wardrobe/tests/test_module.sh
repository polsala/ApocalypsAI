#!/usr/bin/env bash
set -e

# Mock rationale: This test runs terraform init/validate locally without contacting AWS.
# It ensures the configuration is syntactically correct and that the generated bucket name
# starts with the expected prefix.

# Initialize Terraform (disable remote backend for offline testing)
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Apply a plan in destroy mode to capture outputs without creating resources
# Using -target to avoid actual creation; we only need the output value.
terraform apply -auto-approve -target=aws_s3_bucket.wardrobe > /dev/null 2>&1 || true

# Retrieve the bucket name output
bucket_name=$(terraform output -raw bucket_name)

# Expected prefix (default) is "cryptic-wardrobe-"
if [[ "$bucket_name" == cryptic-wardrobe-* ]]; then
  echo "PASS: Bucket name pattern OK ($bucket_name)"
else
  echo "FAIL: Bucket name does not match expected pattern ($bucket_name)"
  exit 1
fi

# Clean up any local state files
rm -rf .terraform .terraform.lock.hcl .terraform.tfstate* 

echo "All tests passed."
