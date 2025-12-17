#!/usr/bin/env bash
# Test that the Terraform module contains the expected S3 bucket resource with versioning and lifecycle rule.

set -euo pipefail

# Locate the main.tf file
FILE="src/main.tf"

# Verify the file exists
if [[ ! -f "$FILE" ]]; then
  echo "FAIL: $FILE not found"
  exit 1
fi

# Check for aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$FILE"; then
  echo "FAIL: aws_s3_bucket resource not found"
  exit 1
fi

# Check for versioning block
if ! grep -q 'versioning {' "$FILE"; then
  echo "FAIL: versioning block not found"
  exit 1
fi

# Check for lifecycle_rule with expiration days = 30
if ! grep -A3 'lifecycle_rule {' "$FILE" | grep -q 'days = 30'; then
  echo "FAIL: lifecycle expiration of 30 days not found"
  exit 1
fi

echo "PASS: All checks passed"
