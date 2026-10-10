#!/usr/bin/env bash
set -euo pipefail

# Test that src/main.tf defines an aws_s3_bucket with versioning enabled and a lifecycle rule

FILE="src/main.tf"

# Mock rationale: Ensure the file exists
if [[ ! -f "$FILE" ]]; then
  echo "FAIL: $FILE not found"
  exit 1
fi

# Check for aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$FILE"; then
  echo "FAIL: aws_s3_bucket resource not defined"
  exit 1
fi

# Check versioning block
if ! grep -q 'versioning {' "$FILE"; then
  echo "FAIL: versioning block missing"
  exit 1
fi

# Check lifecycle_rule block with noncurrent_version_expiration days = 30
if ! grep -q 'noncurrent_version_expiration' "$FILE"; then
  echo "FAIL: lifecycle_rule noncurrent_version_expiration missing"
  exit 1
fi

if ! grep -q 'days = 30' "$FILE"; then
  echo "FAIL: noncurrent_version_expiration days not set to 30"
  exit 1
fi

echo "PASS: All checks passed"
