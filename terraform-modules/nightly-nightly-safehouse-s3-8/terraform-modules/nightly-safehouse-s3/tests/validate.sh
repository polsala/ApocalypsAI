#!/usr/bin/env bash
set -e

# Mock rationale: This script validates that the Terraform module defines an aws_s3_bucket resource.
# In a real environment we would run `terraform init -backend=false` and `terraform validate`.
# Here we simply grep the main.tf file.

MODULE_DIR="$(dirname "$0")/.."
MAIN_TF="$MODULE_DIR/main.tf"

if grep -q 'resource "aws_s3_bucket"' "$MAIN_TF"; then
  echo "PASS: aws_s3_bucket resource found."
else
  echo "FAIL: aws_s3_bucket resource missing."
  exit 1
fi

if grep -q 'versioning {' "$MAIN_TF"; then
  echo "PASS: versioning block present."
else
  echo "FAIL: versioning block missing."
  exit 1
fi

if grep -q 'noncurrent_version_expiration' "$MAIN_TF"; then
  echo "PASS: lifecycle rule for noncurrent version expiration present."
else
  echo "FAIL: lifecycle rule missing."
  exit 1
fi

echo "All checks passed."
