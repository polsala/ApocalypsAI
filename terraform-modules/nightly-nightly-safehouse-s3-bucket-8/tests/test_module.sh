#!/usr/bin/env bash
set -e

# Initialize Terraform (quietly)
terraform init -input=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan and capture output
PLAN=$(terraform plan -input=false -no-color)

# Ensure the S3 bucket resource is present
if ! echo "$PLAN" | grep -q "aws_s3_bucket.this"; then
  echo "ERROR: S3 bucket resource not found in plan"
  exit 1
fi

# Ensure versioning block is present
if ! echo "$PLAN" | grep -q "versioning {"; then
  echo "ERROR: Versioning block missing"
  exit 1
fi

# Ensure lifecycle expiration block is present
if ! echo "$PLAN" | grep -q "expiration {"; then
  echo "ERROR: Lifecycle expiration block missing"
  exit 1
fi

# Ensure server‑side encryption block is present
if ! echo "$PLAN" | grep -q "server_side_encryption_configuration"; then
  echo "ERROR: Encryption configuration missing"
  exit 1
fi

echo "All checks passed."
