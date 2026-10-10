#!/usr/bin/env bash
# Test that the Terraform module defines an aws_s3_bucket with expected settings.

set -e

# Locate the module file
MODULE_FILE="$(dirname "$0")/../src/main.tf"

# Mock rationale: we simply grep for required blocks to avoid needing terraform binary.

if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$MODULE_FILE"; then
  echo "FAIL: aws_s3_bucket resource not found"
  exit 1
fi

if ! grep -q 'versioning {' "$MODULE_FILE"; then
  echo "FAIL: versioning block not found"
  exit 1
fi

if ! grep -q 'sse_algorithm = "AES256"' "$MODULE_FILE"; then
  echo "FAIL: server-side encryption not configured"
  exit 1
fi

if ! grep -q 'expiration {' "$MODULE_FILE"; then
  echo "FAIL: lifecycle expiration not found"
  exit 1
fi

echo "PASS: All required configurations present."
