#!/usr/bin/env bash
# Test that the Terraform module contains required resources

set -e

MODULE_DIR=$(dirname "$0")/..

# Check that main.tf defines aws_s3_bucket
if ! grep -q 'resource "aws_s3_bucket"' "$MODULE_DIR/main.tf"; then
  echo "Missing aws_s3_bucket resource"
  exit 1
fi

# Check versioning block
if ! grep -q 'aws_s3_bucket_versioning' "$MODULE_DIR/main.tf"; then
  echo "Missing versioning configuration"
  exit 1
fi

# Check encryption block
if ! grep -q 'aws_s3_bucket_server_side_encryption_configuration' "$MODULE_DIR/main.tf"; then
  echo "Missing encryption configuration"
  exit 1
fi

# Check lifecycle block
if ! grep -q 'aws_s3_bucket_lifecycle_configuration' "$MODULE_DIR/main.tf"; then
  echo "Missing lifecycle configuration"
  exit 1
fi

# Check IAM policy
if ! grep -q 'aws_iam_policy' "$MODULE_DIR/main.tf"; then
  echo "Missing IAM policy"
  exit 1
fi

echo "All checks passed."
