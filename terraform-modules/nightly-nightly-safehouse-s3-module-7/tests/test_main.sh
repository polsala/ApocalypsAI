#!/usr/bin/env bash
# Test that the Terraform module contains the expected resources and settings.

set -e

# Check that main.tf defines the aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' main.tf; then
  echo "Missing aws_s3_bucket resource"
  exit 1
fi

# Check that versioning is enabled
if ! grep -A2 'versioning {' main.tf | grep -q 'enabled = true'; then
  echo "Versioning not enabled"
  exit 1
fi

# Check that lifecycle rule expires after 365 days
if ! grep -A4 'lifecycle_rule {' main.tf | grep -q 'days = 365'; then
  echo "Lifecycle rule for 365 days missing"
  exit 1
fi

echo "All checks passed."
exit 0
